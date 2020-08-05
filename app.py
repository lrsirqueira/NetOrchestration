# imports
from flask import Flask, request, jsonify
from flask_restful import Resource, Api
from sqlalchemy import create_engine
from json import dumps

# Importar os Métodos que a API executara
import ProvisiongServices
import database

app = Flask(__name__)

@app.route('/api/add_service', methods=['POST'])
def add_service():
    data = request.get_json()
    
    retorno = ProvisiongServices.add_serv(data)
    return jsonify(retorno), 201

@app.route('/api/get_service', methods=['GET'])
def get_service():
    data = request.get_json()
    contrato  = data['contrato']
    contrato_data = database.GetContrato(contrato)
    return jsonify(contrato_data), 201

@app.route('/api/del_service', methods=['POST'])
def del_service():
    contrato_data = {}
    data = request.get_json()
    contrato  = data['contrato']
    contrato_data = database.GetContrato(contrato)    
    contrato_data['contrato'] = contrato
    retorno = ProvisiongServices.del_serv(contrato_data)
    return jsonify(retorno), 201

if __name__ == '__main__':
    app.run(host= '0.0.0.0',debug=True)