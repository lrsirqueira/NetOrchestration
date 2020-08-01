# imports
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

# Importar os Métodos que a API executara
import ProvisiongServices

app = Flask(__name__)

@app.route('/api/add_service', methods=['POST'])
def add_service():
    data = request.get_json()
    
    retorno = ProvisiongServices.add_serv(data)
    return jsonify(retorno), 201


if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)