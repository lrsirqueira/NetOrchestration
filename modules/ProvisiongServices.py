# Imports 
from modules import database
import os
import glob
from shutil import copyfile

# Provisionamento  do servico
def add_serv(data):
    contrato  = data['contrato']
    pop_name = data['pop']

    # Obtendo as variáveis do banco de dados a partir da informacao de pop
    # Tá feio aqui.. o ideal seria um metodo só para isto numa Classe de db
    # Mas funciona
    pe_name       = (database.GetPe(pop_name))
    pe_info       = (database.GetPeInfo(pe_name)) 
    pe_interface  = pe_info[0][2]
    regiao        = pe_info[0][1]
    ips_data      = (database.GetIp(regiao))
    endereco_ip   = ips_data[1]
    bloco_ip      = ips_data[0]
    vlan_id       = (database.GetVlan(pop_name))
    mask          = (database.GetMask(pe_name))
    end_mask    = (bloco_ip + str(endereco_ip) + mask)
    sub_interface = (pe_interface + '.' + str(vlan_id))

    # Criar os arquivos base para o Ansible
    # Todo PE terá um arquivo vazio para o Ansible nao dar erro
    database.CreateBaseFiles()

    # Criando os dados para criar o arquivo de Hosts, sera adicionado em uma lista
    # Aqui será inserido no arquivo os dados que o Ansible utilizara para 
    # provisionar o Router
    data = []    
    data.append(sub_interface)
    data.append('No_Description')
    data.append(end_mask)
    data.append(vlan_id)

    # Salvando os dados da lista no arquivo yml para provisionar o router
    retorno = database.Save_YML_file(data,pe_name)

    # O caminho do Playbook do Ansible
    # Cada tipo de acao tem um arquivo diferente
    caminho  = 'Ansible/add_int.yml'

    # Aqui e chamado o Metodo para rodar o Ansible e enviar o caminho que o arquivo esta
    # Cada acao do Ansible sera printado, como estaremos rodando via API
    # todas as acoes serao printadas na console da API 
    # A chamada nao recebera estas saidas
    '''print(RunAnsible.Run(caminho))
    '''

    # Atualiza banco de dados com Vlans e IPs
    # Uma vez que o provisionamento rodou com sucesso posso atualizar o banco de dados com as informacoes coletadas
    # OBS: caso haja uma falha no provisionamento, este update nao deve ocorrer
    bloco_end   = (endereco_ip - 1)
    database.UpdateDataDb(contrato,pop_name,vlan_id,bloco_ip,bloco_end,sub_interface,pe_name)
    
    # Aqui vou ter que criar o o JSON
    # O retorno para a API serao os dados abaixo
    # preciso mudar para JSON
    retorno = (f'{pop_name} {pe_name} {sub_interface} {end_mask}')
    
    # Limpar a pasta de Hosts
    files = glob.glob('Ansible/host_vars/R*')
    for f in files:
        os.remove(f)
    
    return(retorno)

def del_serv(contrato_data):
    contrato = int(contrato_data['contrato'])
    # Deleta o Banco... o ideal eh que fosse feito depois de validar que foi mesmo
    del_serv_data = database.DelServdb(contrato)

    # Atribuindo as variaveis
    sub_interface = contrato_data['interface']
    bloco_ip    = contrato_data['bloco_ip']
    vlan_id     = contrato_data['vlan_id']
    pe_name     = contrato_data['pe_name']
    pop_name    = contrato_data['pop_name']

    # Criar os arquivos base para o Ansible
    database.CreateBaseFiles()

    # Criando os dados para criar o arquivo de Hosts
    data = []    
    data.append(sub_interface)
    data.append('No_Description')
    data.append(bloco_ip)
    data.append(vlan_id)

    retorno = database.Save_YML_file(data,pe_name)

    caminho  = 'Ansible/del_int.yml'

    '''print(RunAnsible.Run(caminho))
    '''

    # Aqui vou ter que criar o o JSON
    retorno = (f'{pop_name} {pe_name} {sub_interface} {bloco_ip}')
    
    # Limpar a pasta de Hosts
    files = glob.glob('Ansible/host_vars/R*')
    for f in files:
        os.remove(f)
    
    return(retorno)