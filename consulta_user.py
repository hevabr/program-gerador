import requests
import hashlib

# 1. Obter um token de desafio
base_url = "https://devcrm.wikidados.com.br/webservice.php"
params = {
    "operation": "getchallenge",
    "username": "admin"  # Substitua pelo seu nome de usuário
}
print('Ola')
response = requests.get(base_url, params=params)

# Verifique o status da resposta
if response.status_code == 200:
    # A resposta foi bem-sucedida
    data = response.json()
    challenge_token = data.get("result", {}).get("token")
    if challenge_token:
        print("Token de desafio obtido:", challenge_token)
    else:
        print("Não foi possível obter o token de desafio na resposta.")
else:
    # A solicitação falhou
    print("Falha na solicitação:", response.status_code)

# 2. Criar uma chave de acesso
access_key = "7FGAB62zlfDnr0Fb"  # Substitua pela sua chave de acesso
access_key_hash = hashlib.md5((challenge_token + access_key).encode()).hexdigest()

print("Chave de acesso gerada:", access_key_hash)

# 3. Realizar o login
params = {
    "operation": "login",
    "username": "admin",  # Substitua pelo seu nome de usuário
    "accessKey": access_key_hash
}

response = requests.post(base_url, data=params)

# Verifique o status da resposta
if response.status_code == 200:
    # A solicitação foi bem-sucedida
    login_response = response.json()
    if "success" in login_response and login_response["success"]:
        session_id = login_response.get("result", {}).get("sessionName")
        if session_id:
            print("Login realizado com sucesso! SessionID:", session_id)
        else:
            print("Não foi possível obter o SessionID na resposta.")
    else:
        print("Erro durante o login. Mensagem de erro:", login_response.get("error", {}).get("message"))
else:
    # Ocorreu um erro na solicitação
    print("Erro durante o login. Código de status:", response.status_code)


