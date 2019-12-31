<!--
*** Thanks for checking out this README Template. If you have a suggestion that would
*** make this better, please fork the psychopathology-fer-assistant and create a pull request or simply open
*** an issue with the tag "enhancement".
*** Thanks again! Now go create something AMAZING! :D
***
***
***
*** To avoid retyping too much info. Do a search and replace for the following:
*** RodolfoFerro, psychopathology-fer-assistant, twitter_handle, rodolfoferroperez@gmail.com
-->


<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/RodolfoFerro/psychopathology-fer-assistant">
    <img src="../assets/logo.png" alt="Logo" width="256">
  </a>
  <br />

  <!-- Badges -->
  <img src="https://img.shields.io/github/languages/top/RodolfoFerro/psychopathology-fer-assistant?style=for-the-badge" alt="License" height="25">
  <img src="https://img.shields.io/github/repo-size/RodolfoFerro/psychopathology-fer-assistant?style=for-the-badge" alt="GitHub repo size" height="25">
  <img src="https://img.shields.io/github/last-commit/RodolfoFerro/psychopathology-fer-assistant?style=for-the-badge" alt="GitHub last commit" height="25">
  <img src="https://img.shields.io/github/license/RodolfoFerro/psychopathology-fer-assistant?style=for-the-badge" alt="License" height="25">
  <br />
  <a href="https://www.linkedin.com/in/rodolfoferro/">
    <img src="https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555" alt="LinkedIn" height="25">
  </a>
  <a href="https://twitter.com/FerroRodolfo/">
    <img src="https://img.shields.io/twitter/follow/FerroRodolfo?label=Twitter&logo=twitter&style=for-the-badge" alt="Twitter" height="25">
  </a>

  <h3 align="center">Psychopathology Assistant</h3>
  <p align="center">
    Because mental health matters.
    <br />
    <a href="https://github.com/RodolfoFerro/psychopathology-fer-assistant"><strong>View the demo »</strong></a>
    <br />
  </p>
</p>

<!-- TABLE OF CONTENTS -->
## Table of Contents

* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
  * [Running the Application](#running-the-application)


# Raspberry Pi Setup
[![Raspberry Pi Setup][screenshot]](https://github.com/RodolfoFerro/psychopathology-fer-assistant)

<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps. This folder already includes a script and the required cascade files in order to perform face detection for a posterior facial emotion recognition task.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them. For this particular section I will suppose that you already have git installed on your Raspberry Pi.

For a general everview, you can check out my blog tutorial on [how to setup your Raspberry Pi Model B as Google Colab (Feb '19) to work with Tensorflow, Keras and OpenCV](https://rodolfoferro.xyz/Setup-your-Raspberry-Pi-as-Google-Colab/), **as those are the steps that we will follow**.

### Installation

1. Clone the `psychopathology-fer-assistant` repo:
	```bash
	git clone https://github.com/RodolfoFerro/psychopathology-fer-assistant.git
	```
2. Create a virtual environment with Python 3.7 in order to install our dependencies.
3. Install OpenCV dependencies:
	```bash
	sudo apt-get install libcblas-dev libatlas-base-dev libjasper-dev 
	sudo apt-get install libhdf5-dev libhdf5-serial-dev
	sudo apt-get install libqtgui4 libqt4-test
	```
	Now you can install OpenCV:
	```bash
	pip install opencv-contrib-python
	```
4. Install Tensorflow dependencies:
	```bash
	sudo apt-get install libblas-dev liblapack-dev gfortran
	sudo apt-get install python3-dev python3-setuptools
	sudo apt-get install python3-numpy python3-scipy python3-h5py

	sudo apt-get update
	```
	Now you can install Tensorflow:
	```bash
	pip install tensorflow==2.0.0
	```
5. You can finish installing the rest of the requirements using `pip`:
```bash
cd rpi
pip install -r requirements.txt
```

<!-- USAGE EXAMPLES -->
## Usage

### Running the Application

You must specify the labels for each class in the [`classes.txt`](https://github.com/RodolfoFerro/psychopathology-fer-assistant/tree/master/rpi/classes.txt), the classes will be indexed in the same order as in this file. By default the text file already contains the classes according to the trained model.

The main script contains a parser in which any extra required can be specified:
```bash
python main.py -h
```

This outputs the following:
```
usage: main.py [-h] [-c CLASSES] [-ch CHANNELS] [-hc HAAR] [-hcp HAARPATH]
               [-rs RESIZING] [-fs FRAMESIZE] [-m MODEL] [-a API] [-au APIURL]
               [-p PATIENT]

optional arguments:
  -h, --help            show this help message and exit
  -c CLASSES, --classes CLASSES
                        Path to custom txt file containing classes.
  -ch CHANNELS, --channels CHANNELS
                        Number of channels for input image.
  -hc HAAR, --haar HAAR
                        Haar cascade to be used for face detection.
  -hcp HAARPATH, --haarpath HAARPATH
                        Path to Haar cascades for face detection.
  -rs RESIZING, --resizing RESIZING
                        Image width for resizing.
  -fs FRAMESIZE, --framesize FRAMESIZE
                        Set frame size: (1) 640x360 (2) (320x180) (-1) (160,
                        90)
  -m MODEL, --model MODEL
                        Path to custom model in tflite format.
  -a API, --api API     Send model response to API.
  -au APIURL, --apiurl APIURL
                        URL for API consumption.
  -p PATIENT, --patient PATIENT
                        Specify patient for API.
```

With this, you can specify any path to any of the files to be used, or specify the resizing of the images to be processed by the neural net.

The basic example to run our trained model included in this repo would be the following:
```bash
python main.py -ch 1 -fs 2 -m ../model/tf_model.tflite
```


[screenshot]: ../assets/8.png