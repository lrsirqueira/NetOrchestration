# Importar os Métodos que a API executara
import ProvisiongServices

data = {"contrato":"3861035","pop":"oeste_01"}

retorno = ProvisiongServices.add_serv(data)

print(retorno)
