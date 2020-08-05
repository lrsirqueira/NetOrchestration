import sqlite3
import ipaddress

def GetPe(pop_name):
    conn = sqlite3.connect('nso_localdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT pe FROM pops WHERE name = ?', (pop_name,))
    pe_name=cursor.fetchall()
    return(pe_name[0][0])

def GetPeInfo(pe_name):
    conn = sqlite3.connect('nso_localdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM pes WHERE name = ?', (pe_name,))
    pe_info=cursor.fetchall()
    return(pe_info)

def GetIp(regiao):
    ips_list = []
    retorno = []
    conn = sqlite3.connect('nso_localdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM blocos_ip WHERE regiao = ?', (regiao,))
    data=cursor.fetchall()
    bloco_ip = data[0][0]

    ### Selecionando o IP
    cursor.execute('SELECT * FROM ips WHERE bloco_ip = ?', (bloco_ip,))
    ips=cursor.fetchall()
    if len(ips)==0:
        ip_address = ( 0 + 1 )
    else:
        for ip in ips:
            ips_list.append(int(ip[3]))
    ips_list.sort()
    ips_livres = list(set(range(0, 256 , 4)) - set(ips_list))
    ip_address = (ips_livres[0] + 1 )

    retorno.append(bloco_ip)
    retorno.append(ip_address)
    return(retorno)

def GetVlan(pop_name):
    vlans_list = []
    conn = sqlite3.connect('nso_localdata.db')
    cursor = conn.cursor()
    cursor.execute('SELECT vlan_id FROM vlans WHERE pop_name = ?', (pop_name,))
    vlans=cursor.fetchall()

    for item in vlans:
        vlans_list.append(int(item[0]))
    
    vlans_list.sort()
    vlans_livres = list(set(range(1, 4094 + 1)) - set(vlans_list))
    vlan_id = vlans_livres[0]
    return(vlan_id)

def GetDataDb(pop_name,acao):
    returnData = {}
    vlans_list = []
    ips_list   = []
    returnData['pop_name'] = pop_name
    returnData['acao']     = acao

    ### ----------> Obtem os dados do PE
    cursor.execute('SELECT * FROM pes WHERE name = ?', (data[0][0],))
    data=cursor.fetchall()
    returnData['regiao']       = data[0][1]
    returnData['pe_interface'] = data[0][2]

    ### ----------> Obtem a Lista de Vlans dos POPs
    cursor.execute('SELECT vlan_id FROM vlans WHERE pop_name = ?', (pop_name,))
    vlans=cursor.fetchall()

    for item in vlans:
        vlans_list.append(int(item[0]))
    
    vlans_list.sort()
    vlans_livres = list(set(range(1, 4094 + 1)) - set(vlans_list))
    returnData['vlan_id'] = vlans_livres[0]
    
    ### ----------> Obtem o Bloco IP que atende a regiao
    cursor.execute('SELECT * FROM blocos_ip WHERE regiao = ?', (data[0][1],))
    data=cursor.fetchall()
    returnData['bloco_ip'] = data[0][0]
 
    ### Selecionando o IP
    cursor.execute('SELECT * FROM ips WHERE bloco_ip = ?', (data[0][0],))
    ips=cursor.fetchall()
    if len(ips)==0:
        returnData['ip_address'] = ( 0 + 1 )
    else:
        for ip in ips:
            ips_list.append(int(ip[3]))
    ips_list.sort()
    ips_livres = list(set(range(0, 256 , 4)) - set(ips_list))
    returnData['ip_address'] = (ips_livres[0] + 1 )


    # Fechando Conexão com o Banco
    conn.close()
    
    return(returnData)
    
def UpdateDataDb(contrato,pop_name,vlan_id,bloco_ip,bloco_end,sub_interface,pe_name):
    ### Parametros Iniciais e Selecionando o POP
    conn = sqlite3.connect('nso_localdata.db')
    cursor = conn.cursor()

    # Insert Vlan ID
    cursor.execute('INSERT INTO vlans(vlan_id,contrato,pop_name) VALUES(?, ?, ?)',(vlan_id,contrato,pop_name))
    data=cursor.fetchall()

    # Insert IP Address
    mask = '/30'
    cursor.execute('INSERT INTO ips(bloco_ip,contrato,mask,endereco) VALUES(?, ?, ?, ?)',(bloco_ip,contrato,mask,bloco_end))
    data=cursor.fetchall()

    # Insert Interface PE
    cursor.execute('INSERT INTO interfaces(pe_name,contrato,interface) VALUES(?, ?, ?)',(pe_name,contrato,sub_interface))
    data=cursor.fetchall()

    ## Fechando Conexão ao Banco
    conn.commit()
    conn.close()
    return('OK')

def GetContrato(contrato):
    returnData = {}
    ### Parametros Iniciais e Selecionando o POP
    conn = sqlite3.connect('nso_localdata.db')
    cursor = conn.cursor()

    # Selecionando o Bloco IP
    cursor.execute('SELECT * FROM ips WHERE contrato = ?', (contrato,))
    data=cursor.fetchall()
    returnData['bloco_ip'] = (data[0][0] + str(data[0][3]) + data[0][2])

    # Selecionando a vlan
    cursor.execute('SELECT vlan_id,pop_name FROM vlans WHERE contrato = ?', (contrato,))
    data=cursor.fetchall()
    returnData['vlan_id'] = data[0][0]
    returnData['pop_name'] = data[0][1]

    # Selecionando a Interface do PE
    cursor.execute('SELECT pe_name,interface FROM interfaces WHERE contrato = ?', (contrato,))
    data=cursor.fetchall()
    returnData['pe_name'] = data[0][0]
    returnData['interface'] = data[0][1]

    ## Fechando Conexão ao Banco
    conn.commit()
    conn.close()
    return(returnData)

def DelServdb(contrato):
    contrato = int(contrato)
    conn = sqlite3.connect('nso_localdata.db')
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM ips WHERE contrato = ?', (contrato,))
    cursor.execute('DELETE FROM interfaces WHERE contrato = ?', (contrato,))
    cursor.execute('DELETE FROM vlans WHERE contrato = ?', (contrato,))
    
    ## Fechando Conexão ao Banco
    conn.commit()
    conn.close()
    return('OK')