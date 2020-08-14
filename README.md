# Orquestrador de Rede
A proposta deste orquestrador é adicionar e deletar interfaces de routers usando REST API.

OBS: Este programa é totalmente para fins educativos, o mesmo não possui tratativas de erros, timeouts, segurança, tratativa de dados na entrada e saída.. etc.Utilize o mesmo para aprender e melhore-o á vontade. É um bom ponta pé, porém, não está pronto para um ambiente de produção

## Pré Requisitos
* clone o repositrório
* adicione suas credenciais no arquivo env, utilizando como modelo o arquivo env.sample
* instalar as libs contidas em requirements.txt

## Os endpoints da API
Estes endpoints permitem adicionar ou deletar interfaces em routers Cisco IOS, IOS_XR e Juniper. Não é preciso enviar nenhum tipo de autenticação, apenas enviar o payload como json.

### POST
`/api/add_int` ou `/api/del_int`
```json
{
	"platform": "cisco_ios",
    "interface": "eth0/1.123",
	"description": "Cliente 01",
	"vlan_id": 123,
	"ip_address": "192.168.111.1 255.255.255.252",
	"device_ip": "1.1.1.1"
}
```
###### Origem dos dados
Obviamente, enviaremos os dados brutos neste ambiete de estudo, no mundo real este dados viria de um SoT ( Source of Truth) como Netbox ou Ubersmith..

Leia Mais sobre SoT: https://blogs.gartner.com/andrew-lerner/2020/01/28/network-source-truth-sot/
