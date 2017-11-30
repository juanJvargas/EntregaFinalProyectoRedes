import requests
import transmissionrpc


tc = transmissionrpc.Client('localhost', port=9091)

url="https://proyectoredestorresvargas.herokuapp.com/pendiente"
response=requests.get(url)
info= response.content
descargar = info.split(",")
size=len(descargar)-1
aux=0
while aux!=size:
	tc.add_torrent(descargar[aux])
	torrents =tc.get_torrents()
	tama= len(torrents)
	name= str(torrents[tama-1].id)
	magnetlink=descargar[aux]
	magnetlink=magnetlink.replace("?","$")
	magnetlink=magnetlink.replace(".","^")
	magnetlink=magnetlink.replace("%","|")
	data=""+magnetlink +","+name
	print(name)
	url="https://proyectoredestorresvargas.herokuapp.com/actualizar/"+ data
	response=requests.get(url)
	print(response.status_code)
	aux =aux+1
	


