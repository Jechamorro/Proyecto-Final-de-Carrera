from flask import Flask, request

app = Flask(__name__)

@app.route('/api/datos', methods=['POST'])
def recibir_datos():
	data= request.json
	print ("Datos recibidos:", data)
	return {"mensaje": "Datos recibidos correctamente"}, 200

if __name__ == '__main__':
	app.run(host="0.0.0.0", port=5000)
