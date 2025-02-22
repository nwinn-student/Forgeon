# whether we are testing or not, when testing we can change main.py, app.py, and any of the template html files and they will automatically update the page when you refresh.  

DEBUG = True

from app import app

addr = '127.0.0.1'
port = 8080

if not DEBUG:
	from gevent.pywsgi import WSGIServer
	print(f'Starting application, open url: http://{addr}:{port}')
	http_server = WSGIServer((addr, port), app)
	http_server.serve_forever()
else:
	app.run(debug=True, host= addr, port=port)