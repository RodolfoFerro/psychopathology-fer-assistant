from datetime import datetime
from time import time
import argparse
import psutil
import re
import os

import tensorflow as tf
import numpy as np
import pyrebase
import cv2


# Connect to Firebase:
config = {
  "apiKey": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
  "authDomain": "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX.firebaseapp.com",
  "databaseURL": "https://XXXXXXXXXXXXXXXXXXXXXXXXXXXXX.firebaseio.com/",
  "storageBucket": "gs://XXXXXXXXXXXXXXXXXXXXXXXXXXXXX.appspot.com"
}
firebase = pyrebase.initialize_app(config)
db = firebase.database()


# Get current Process ID:
pid = os.getpid()

def get_memory_status(pid):
    """Memory getter function."""

    # Build psutil process from PID:
    p = psutil.Process(pid)
    print(" * Process ID:", pid)

    # Print memory status:
    mem_usage = p.memory_percent()
    print(" * Memory {:.4f}%".format(mem_usage))

def prediction_data(patient, output_data):
    return {
        'patient': patient,
        'timestamp': str(datetime.now()),
        'anger': float(output_data[0, 0]),
        'disgust': float(output_data[0, 1]),
        'fear': float(output_data[0, 2]),
        'happiness': float(output_data[0, 3]),
        'sadness': float(output_data[0, 4]),
        'surprise': float(output_data[0, 5]),
        'neutral': float(output_data[0, 6])
    }


def parser():
    """Argument parser function."""

    # Construct the argument parser:
    ap = argparse.ArgumentParser()
    ap.add_argument("-c", "--classes", type=str,
                    default="./classes.txt",
                    help="Path to custom txt file containing classes.")
    ap.add_argument("-ch", "--channels", type=int, default=1,
                    help="Number of channels for input image.")
    ap.add_argument("-hc", "--haar", type=str,
                    default="haarcascade_frontalface_default.xml",
                    help="Haar cascade to be used for face detection.")
    ap.add_argument("-hcp", "--haarpath", type=str,
                    default="./cascades/",
                    help="Path to Haar cascades for face detection.")
    ap.add_argument("-rs", "--resizing", type=int, default=48,
                    help="Image width for resizing.")
    ap.add_argument("-fs", "--framesize", type=int, default=-1,
                    help="Set frame size: \n (1) 640x360 \n (2) (320x180) (-1) (160, 90)")
    ap.add_argument("-m", "--model", type=str,
                    default="../model/tf_model.tflite",
                    help="Path to custom model in tflite format.")
    ap.add_argument("-a", "--api", type=bool, default=False,
                    help="Send model response to API.")
    ap.add_argument("-au", "--apiurl", type=str,
                    default="http://127.0.0.1/api/record",
                    help="URL for API consumption.")
    ap.add_argument("-p", "--patient", type=str, default="John Doe",
                    help="Specify patient for API.")
    args = vars(ap.parse_args())

    return args


def build_classes(classes):
    """Classes dictionary builder."""

    with open(classes, "rt") as c:
        lines = c.readlines()

    classes_list = [re.sub("\n", "", line) for line in lines]
    classes_dict = {class_element: indx for indx, class_element in enumerate(classes_list)}

    return classes_dict


def model_loader(model_path):
    """Model loader function."""

    # Load TFLite model and allocate tensors.
    interpreter = tf.lite.Interpreter(model_path=model_path)
    interpreter.allocate_tensors()

    # Get input and output tensors.
    input_details = interpreter.get_input_details()
    output_details = interpreter.get_output_details()

    model_dict = dict(
        interpreter=interpreter,
        input_details=input_details,
        output_details=output_details
    )

    return model_dict


def viewer(fs, model):
    """FER viewer."""

    interpreter = model['interpreter']
    input_details = model['input_details']
    output_details = model['output_details']

    while(True):
        # Capture frame-by-frame:
        ret, frame = cap.read()
        if fs == 1:
            frame = cv2.resize(frame, (640, 360))
        if fs == 2:
            frame = cv2.resize(frame, (320, 180))
        else:
            frame = cv2.resize(frame, (160, 90))

        # Our operations on the frame come here:
        start_face_detection = time()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        for i, (x, y, w, h) in enumerate(faces):
            if channels == 1:
                # face = cv2.resize(frame[y:y + h, x:x + w], (48, 48))
                face = cv2.resize(gray[y:y + 17 * h // 16,
                                        x - w // 32:x + 33 * w // 32],
                                (img_size, img_size))
            else:
                face = cv2.resize(frame[y:y + 17 * h // 16,
                                        x - w // 32:x + 33 * w // 32],
                                (img_size, img_size))
            cv2.rectangle(frame, (x - w // 32, y),
                        (x + 33 * w // 32, y + 17 * h // 16),
                        (250, 150, 10), 2)
            end_face_detection = time()
            delta_face = end_face_detection - start_face_detection
            print()
            print(" * Time for face {} det.: {}".format(i, delta_face))

            try:
                # cv2.imshow('Mini input face %d' % i, face)
                face = np.expand_dims(face, axis=0).astype(np.float32)
                if channels == 1:
                    face = np.expand_dims(face, axis=-1).astype(np.float32)
                
                # Prediction part:
                start_prediction = time()

                # Test model on random input data.
                input_shape = input_details[0]['shape']
                # input_data = np.array(np.random.random_sample(input_shape), dtype=np.float32)
                interpreter.set_tensor(input_details[0]['index'], face)

                interpreter.invoke()  # HERE COMES THE MAGIC!

                # The function `get_tensor()` returns a copy of the tensor data.
                # Use `tensor()` in order to get a pointer to the tensor.
                output_data = interpreter.get_tensor(output_details[0]['index'])
                prediction = np.argmax(output_data)

                end_prediction = time()
                delta_prediction = end_prediction - start_prediction
                print(" * Time for prediction: {}".format(delta_prediction))

                get_memory_status(pid)
                for emotion, class_id in classes.items():
                    if class_id == prediction:
                        cv2.putText(frame, "Emotion: " + emotion.title(),
                                    (x + 5, y - 10), 0, w/350, (150, 255, 10),
                                    1, cv2.LINE_AA)
                        print(" * Emotion: {}".format(emotion.title()))
                        break

                if api:
                    # print(prediction_data(patient, output_data))
                    r = db.child('fer').push(prediction_data(patient, output_data))
                    # print(r)

            except Exception as e:
                print(e)

        # Display the resulting frame
        cv2.imshow('Emotion detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    # Define classes:
    args = parser()
    classes = build_classes(args['classes'])
    model  = model_loader(args['model'])

    # Extra meta data:
    img_size = args['resizing']
    frame_size = args['framesize']
    channels = args['channels']
    api = args['api']
    api_url  = args['apiurl']
    patient  = args['patient']

    # Initialize videocapture:
    cap = cv2.VideoCapture(0)
    face_cascade_path = args['haarpath'] + args['haar']
    face_cascade = cv2.CascadeClassifier(face_cascade_path)

    # Viewer:
    viewer(frame_size, model)
