"""
	Whether we are testing or not, when testing we can change main.py, 
	app.py, and any of the template html files and they will 
	automatically update the page when you refresh.
"""
DEBUG = False

from app import app

addr = '127.0.0.1'
port = 8080

if not DEBUG:
	from gevent.pywsgi import WSGIServer
	print(f'Starting application, open url: http://{addr}:{port}')
	http_server = WSGIServer((addr, port), app)
	http_server.serve_forever()
else:
	import test # will run all tests EACH time you edit a .py file.
	app.run(debug=True, host= addr, port=port)
	# code will NOT run past here, think of above code like a while true do loop.