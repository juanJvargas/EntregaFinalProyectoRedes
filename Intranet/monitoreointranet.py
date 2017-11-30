#!/usr/bin/python
import subprocess
import requests

#MonitoreoIntranet
#Programa que gestiona la informacion de la maquina de la intranet, cuenta con las siguentes funcionalidades:
#1 Utiliza el programa RESTMonitoring para consultar informacion relacionada el funcionamiento de la maquina sobre la que se
# ejecuta, dentro de la intranet.
#2 Envia los datos de la maquina consultada a la pasarela en Heroku para mantener actualizada dicha informacion.
#Protocolo de comunicacion:
#SEND INFOPC (<item-name>:<item-information>) 
vmstat = subprocess.Popen(['vmstat'], stdout = subprocess.PIPE)
tail = subprocess.Popen(['tail','-n','+3'], stdin = vmstat.stdout, stdout = subprocess.PIPE)
tr = subprocess.Popen(['tr', '-s', ' '], stdin = tail.stdout, stdout = subprocess.PIPE)

output1 = subprocess.check_output(['cut', '-d', ' ', '-f', "4"], stdin = tr.stdout)

vmstat = subprocess.Popen(['vmstat'], stdout = subprocess.PIPE)
tail = subprocess.Popen(['tail','-n','+3'], stdin = vmstat.stdout, stdout = subprocess.PIPE)
tr = subprocess.Popen(['tr', '-s', ' '], stdin = tail.stdout, stdout = subprocess.PIPE)

output2 = subprocess.check_output(['cut', '-d', ' ', '-f', "5"], stdin = tr.stdout)

vmstat = subprocess.Popen(['vmstat'], stdout = subprocess.PIPE)
tail = subprocess.Popen(['tail','-n','+3'], stdin = vmstat.stdout, stdout = subprocess.PIPE)
tr = subprocess.Popen(['tr', '-s', ' '], stdin = tail.stdout, stdout = subprocess.PIPE)

output3 = subprocess.check_output(['cut', '-d', ' ', '-f', "6"], stdin = tr.stdout)

vmstat = subprocess.Popen(['vmstat'], stdout = subprocess.PIPE)
tail = subprocess.Popen(['tail','-n','+3'], stdin = vmstat.stdout, stdout = subprocess.PIPE)
tr = subprocess.Popen(['tr', '-s', ' '], stdin = tail.stdout, stdout = subprocess.PIPE)

output4 = subprocess.check_output(['cut', '-d', ' ', '-f', "7"], stdin = tr.stdout)

str= output1+","+output2+","+output3+","+output4
str1= str.split(",")

ms=str1[0].replace("\n","")+","+str1[1].replace("\n","")+","+str1[2].replace("\n","")+","+str1[3].replace("\n","")

print(ms)

url="https://proyectoredestorresvargas.herokuapp.com/memoria/"+ms
response = requests.get(url)
print(response)