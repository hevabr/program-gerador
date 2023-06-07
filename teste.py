import requests
import hashlib
import json
import pprint

#-----------------------------------------------------------------------------#
# Login com a MONI

base_url = "https://devcrm.wikidados.com.br/webservice.php?"
params = {
    "operation": "getchallenge",
    "username": "admin"
}

response = requests.get(base_url, params=params)

if response.status_code == 200:
    data = response.json()
    challenge_token = data.get("result", {}).get("token")
    if challenge_token:
        pass
    else:
        print("Não foi possível obter o token de desafio na resposta.")
else:
    print("Falha na solicitação:", response.status_code)

access_key = "7FGAB62zlfDnr0Fb"
access_key_hash = hashlib.md5(
    (challenge_token + access_key).encode()).hexdigest()

params = {
    "operation": "login",
    "username": "admin",
    "accessKey": access_key_hash
}

response = requests.post(base_url, data=params)

if response.status_code == 200:
    login_response = response.json()
    if "success" in login_response and login_response["success"]:
        session_id = login_response.get("result", {}).get("sessionName")
        if session_id:
            pass
        else:
            print("Não foi possível obter o SessionID na resposta.")
    else:
        print("Erro durante o login. Mensagem de erro:",
              login_response.get("error", {}).get("message"))
else:
    print("Erro durante o login. Código de status:", response.status_code)

#-----------------------------------------------------------------------------#
# Pesquisa do usuário e login no CRM

query = "SELECT * FROM Users;"

params = {
    "operation": "query",
    "sessionName": session_id,
    "query": query
}

response = requests.get(base_url, params=params)

if response.status_code == 200:
    result = response.json()
    if "success" in result and result["success"]:
        users = result.get("result", {})
        for user in users:
            user_name = user.get("user_name")
            first_name = user.get("first_name")
            accesskey = user.get("accesskey")

login_username = input("Digite o nome de usuário para fazer login: ")

target_user = None
for user in users:
    if user.get("user_name") == login_username:
        target_user = user
        break

if target_user:
    target_user_name = target_user.get("user_name")
    target_first_name = target_user.get("first_name")
    target_accesskey = target_user.get("accesskey")

    params = {
        "operation": "getchallenge",
        "username": target_user_name
    }

    response = requests.get(base_url, params=params)

    if response.status_code == 200:
        data = response.json()
        challenge_token = data.get("result", {}).get("token")
        if challenge_token:
            pass
        else:
            print("Não foi possível obter o token de desafio na resposta.")
    else:
        print("Falha na solicitação:", response.status_code)

    target_access_key_hash = hashlib.md5(
        (challenge_token + target_accesskey).encode()).hexdigest()

    params = {
        "operation": "login",
        "username": target_user_name,
        "accessKey": target_access_key_hash
    }

    response = requests.post(base_url, data=params)

    if response.status_code == 200:
        login_response = response.json()
        if "success" in login_response and login_response["success"]:
            session_id = login_response.get("result", {}).get("sessionName")
            if session_id:
                print("Olá,", target_first_name + "!")
            else:
                print("Não foi possível obter o SessionID na resposta.")
    else:
        print("Erro durante o login. Mensagem de erro:",
            login_response.get("error", {}).get("message"))
else:
    print("Erro durante o login. Código de status:", response.status_code)

#-----------------------------------------------------------------------------#
# Buscar o Pedidos de Vendas no CRM
number_pv = input("Digite o número do Pedido de Venda (PV): ")

query_params = {
    "operation": "query",
    "sessionName": session_id,
    "query": f"SELECT * FROM SalesOrder WHERE salesorder_no = 'PV{number_pv}';",
}

query_response = requests.get(base_url, params=query_params)

if query_response.status_code == 200:
    query_result = query_response.json()     
else:
    print("Falha na solicitação:", query_response.status_code)

# O retrive do CARALHOOOOOOOOOOO  
result = query_result["result"][0]
pv_details = requests.get(f'{base_url}operation=retrieve&sessionName={session_id}&id={result["id"]}')

if pv_details.status_code == 200:
    pv_data = pv_details.json()

    create_pv = pv_data.copy()

    # Transforme o JSON em uma string
    json_data = json.dumps(create_pv)

    # Faça a solicitação POST para criar um novo PV
    create_pv_url = (f'{base_url}operation=create&sessionName={session_id}&elementType=SalesOrders')
    create_pv_response = requests.post(create_pv_url, data=json_data)
    pprint.pprint(create_pv_url)
    pprint.pprint(create_pv_response)




   