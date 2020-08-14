# Imports Especificos dos Modulos
from modules.DeviceConection import get_template, get_netmiko_conn

def add_int(data):
    # Gerar o Script
    print("Gerando Script ... ")
    script_config = get_template(data, "add_int")

    ## Conectar ao Device
    print("Tentando Conectar ao Device ... ")
    dev_conn = get_netmiko_conn(data)

    # Enviando Comando ao Dispositivo
    retorno_device  = dev_conn.send_config_set(script_config.split("\n"))

    print(retorno_device)

    # Desconectando do Dispositivo
    print("Desconectando do  Device ... ")
    dev_conn.disconnect()

    return retorno_device

def del_int(data):
    # Gerar o Script
    print("Gerando Script ... ")
    script_config = get_template(data, "del_int")

    ## Conectar ao Device
    print("Tentando Conectar ao Device ... ")
    dev_conn = get_netmiko_conn(data)

    # Enviando Comando ao Dispositivo
    retorno_device  = dev_conn.send_config_set(script_config.split("\n"))

    print(retorno_device)

    # Desconectando do Dispositivo
    print("Desconectando do  Device ... ")
    dev_conn.disconnect()
    
    return retorno_device
