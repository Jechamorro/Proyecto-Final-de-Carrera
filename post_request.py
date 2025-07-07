import requests
import base64

#Configuracion
ip= "http://192.168.1.24:5000"
endpoint = "/api/datos"
url = f"{ip}{endpoint}"

data = "algun texto"
codificado = base64.b64encode(data.encode()).decode()

#Encabezados opcionales
headers={
	"Content-Type" : "application/json"
}

#Payload con la cadena codificada en Base64
payload = {
	"data": codificado
}

#Enviar la solicitud POST
response = requests.post(url, json=payload, headers=headers)

#Imprimir la respuesta
print ("Codigo de estado: ", response.status_code)
print ("Respuesta: ", response.text)
