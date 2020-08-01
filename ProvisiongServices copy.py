# Imports 
import Controller
import MetodoRunAnsible
import os
import glob
from shutil import copyfile

# Provisionamento  do servico
def add_serv(data):
    contrato  = data['contrato']
    pop_name = data['pop']
    acao        = 'add'

    provisioningData = Controller.GetDataDb(pop_name,acao)

    # Ajustando o Bloco IP
    if provisioningData['pe_name'] == 'R1' or 'R2':
        endereco_ip = (provisioningData['bloco_ip']+str(provisioningData['ip_address'])+' 255.255.255.252')
    
    if provisioningData['pe_name'] == 'R3':
        endereco_ip = (provisioningData['bloco_ip']+str(provisioningData['ip_address'])+'/30')

    # Cria os arquivos base ......>>>>>> Melhorar
    copyfile('Ansible/host_vars/base.yml', 'Ansible/host_vars/R1.yml')
    copyfile('Ansible/host_vars/base.yml', 'Ansible/host_vars/R2.yml')
    copyfile('Ansible/host_vars/base.yml', 'Ansible/host_vars/R3.yml')

    # Criando os dados para criar o arquivo de Hosts
    data = []
    sub_interface = (provisioningData['pe_interface'] + '.' + str(provisioningData['vlan_id']))
    data.append(sub_interface)
    data.append('NO_Description')
    data.append(endereco_ip)
    data.append(provisioningData['vlan_id'])
    router = provisioningData['pe_name']
    vlan_id = provisioningData['vlan_id']

    retorno = Controller.Save_YML_file(data,router)

    caminho  = 'Ansible/add_int.yml'

    print(MetodoRunAnsible.Run(caminho))
    
    # Atualiza banco de dados com Vlans e IPs
    bloco_ip   = provisioningData['bloco_ip']
    bloco_end   = (provisioningData['ip_address'] - 1)
    Controller.UpdateDataDb(contrato,pop_name,vlan_id,bloco_ip,bloco_end,sub_interface,router)
    
    # Aqui vou ter que criar o o JSON
    pop_name = provisioningData['pop_name']
    pe_name  = provisioningData['pe_name']

    retorno = (f'{pop_name} {pe_name} {sub_interface} {endereco_ip}')
    
    # Limpar a pasta de Hosts
    files = glob.glob('Ansible/host_vars/R*')
    for f in files:
        os.remove(f)
    
    return(retorno)





