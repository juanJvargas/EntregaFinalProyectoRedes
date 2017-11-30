import requests
print("digite el magnetlink")
x= input()+""
x=x.replace("?","$")
x=x.replace(".","^")
x=x.replace("%","|")
url="https://proyectoredestorresvargas.herokuapp.com/descargar/"+x
response = requests.get(url)
print(response.content)