from app import *

if __name__ == '__main__':
	from app.views import *
	from app.endpoints import *
	app.run_server(debug=True)