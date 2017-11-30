import requests
import transmissionrpc

tc = transmissionrpc.Client('localhost', port=9091)
torrents=tc.get_torrents()
size = len(torrents)
print(size)
aux=0
while aux!=size:
	magnetlink="";
	name=str(torrents[aux].id)
	progreso=torrents[aux].progress
	url="https://proyectoredestorresvargas.herokuapp.com/actualizar/"+name+", progreso,"+str(progreso)
	response=requests.get(url)
	print(response.content)
	aux=aux+1