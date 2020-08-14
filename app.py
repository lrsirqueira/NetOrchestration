# Import Geral
from flask import Flask, request

# Imports Especificos dos Modulos
from modules import Controller

app = Flask(__name__)

@app.route('/api/add_int', methods=['POST'])
def add_int():
    data = request.get_json()
    return_data = Controller.add_int(data)

    return return_data

@app.route('/api/del_int', methods=['POST'])
def del_int():
    data = request.get_json()
    return_data = Controller.del_int(data)
    return return_data

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
