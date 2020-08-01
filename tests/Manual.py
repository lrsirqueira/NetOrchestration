# Importar os Métodos que a API executara
import ProvisiongServices
import Controller

# ADD Serv
data = {"contrato":"99999999","pop":"leste_02"}
retorno = ProvisiongServices.add_serv(data)
print(retorno)

# GET Serv
data = {"contrato":"99999999"}
contrato  = data['contrato']
retorno = Controller.GetContrato(contrato)
print(retorno)

# DEL Serv
data = {"contrato":"99999999"}
contrato_data = {}
contrato      = data['contrato']

contrato_data = Controller.GetContrato(contrato)
contrato_data['contrato'] = contrato
retorno = ProvisiongServices.del_serv(contrato_data)
print(retorno)