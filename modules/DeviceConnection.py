# Imports Gerais
import json
from jinja2 import Environment, FileSystemLoader
from netmiko import Netmiko

def get_template(data, script):
    # Criando o Global Env
    j2_env = Environment(
        loader=FileSystemLoader("."), trim_blocks=True, autoescape=True
        )

    # Gerando o Script baseado nos dados da variavel e no script
    template = j2_env.get_template(
        f"/templates/{data['platform']}_{script}.j2"
        )

    # Gerando os comandos
    script_config = template.render(data=data)

    return script_config

def get_netmiko_conn(data):
    # Coletando variaveis de Ambiente
    with open('env') as env_file:
        env_data = json.load(env_file)

    # Conectando no dispositivo 
    conn = Netmiko(
        host=data['device_ip'],
        username=env_data['usuario'],
        password=env_data['senha'],
        device_type=data['platform'],
        )

    return conn
