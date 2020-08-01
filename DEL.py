import Controller
import MetodoRunAnsible
import os
import glob

infoPop     =(Controller.ListarPops())
pop_name    = infoPop[0]
acao        = 'add'
print(f'Vamos Desprovisionar um Serviço no POP: {pop_name}')

provisioningData = Controller.GetDataDb(pop_name,acao)
''' Exemplo :
{
'pop_name'    : 'leste_01'
'acao'        : 'add'
'pe_name'     : 'R1'
'vlan_id'     : 3
'regiao'      : 'leste'
'pe_interface': 'Ethernet0/2'
'bloco_ip'    : '100.64.0.'
'ip_address'  : 9
'vlans_list'  :
'ips_list'    :
}
'''

# Ajustando o Bloco IP
if provisioningData['pe_name'] == 'R1' or 'R2':
    endereco_ip = (provisioningData['bloco_ip']+str(provisioningData['ip_address'])+' 255.255.255.252')

if provisioningData['pe_name'] == 'R3':
    endereco_ip = (provisioningData['bloco_ip']+str(provisioningData['ip_address'])+'/30')

# Limpar a pasta de Hosts
files = glob.glob('Ansible/host_vars/*')
for f in files:
    os.remove(f)

# Criando os dados para criar o arquivo de Hosts
# ['eth0/2.1','POLICE_DEP_01','192.168.1.1 255.255.255.252',1],
data = []
sub_interface = (provisioningData['pe_interface'] + '.' + str(provisioningData['vlan_id']))
data.append(sub_interface)
data.append('NO_Description')
data.append(endereco_ip)
data.append(provisioningData['vlan_id'])
router = provisioningData['pe_name']

retorno = Controller.Save_YML_file(data,router)

# Definindo o Arquivo à ser usado
if acao == 'add':
    caminho  = 'Ansible/add_int.yml'
if acao == 'del':
    caminho  = 'Ansible/del_int.yml'

print(MetodoRunAnsible.Run(caminho))

# Atualiza banco de dados com Vlans e IPs
vlans_list = provisioningData['vlans_list']
ips_list   = provisioningData['ips_list']
bloco_ip   = provisioningData['bloco_ip']

vlans_list.append(provisioningData['vlan_id'])
ips_list.append((provisioningData['ip_address'] - 1))
Controller.UpdateDataDb(pop_name,vlans_list,ips_list,bloco_ip)

# Apresenta os dados técnicos para configurar no CE
pop_name = provisioningData['pop_name']
pe_name  = provisioningData['pe_name']
print('Provisionamento realizado com sucesso...\n\nFoi provisionado o seguinte serviço:')
print(f'POP          : {pop_name}')
print(f'PE           : {pe_name}')
print(f'SubInterface : {sub_interface}')
print(f'Bloco IP     : {endereco_ip}')

# Limpar a pasta de Hosts
files = glob.glob('Ansible/host_vars/*')
for f in files:
    os.remove(f)


