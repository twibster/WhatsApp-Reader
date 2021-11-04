from website import app
import socket

ip = socket.gethostbyname(socket.gethostname())

if __name__ =='__main__':
	app.run(debug =False,host=ip)