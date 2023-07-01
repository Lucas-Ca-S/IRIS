from requests import request
import os

BASE_URL = "https://graph.microsoft.com/v1.0"
URL_TOKEN = "https://login.microsoftonline.com/c58f8565-7ab4-440f-84f2-dd75f3745a69/oauth2/v2.0/token"
APP_SECRET = os.environ['APP_REGISTRATION_SECRET']
PAYLOAD = f"client_id=ea27a6e0-0d4c-4735-9843-c7747630ac24&scope=https%3A%2F%2Fgraph.microsoft.com%2F.default&client_secret={APP_SECRET}&grant_type=client_credentials"    


HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded',
}

def get_teams_token():

    #Realizando request para resgatar o token de autenticação atualizado
 
    response_token_teams = request("POST", URL_TOKEN, headers=HEADERS, data=PAYLOAD)
    
    if(response_token_teams.status_code == 200):
        print("Token gerado com sucesso! O novo token gerado irá durar "+str(response_token_teams.json()['expires_in'])+" segundos")
   
        access_token= str(response_token_teams.json()['access_token'])
        token_type= str(response_token_teams.json()['token_type'])
   
        teams_token=token_type+" "+access_token
        return teams_token
    
def base_request(endpoint:str):
    headers = {
        'Authorization': f'{get_teams_token()}',
    }

    return request("GET", BASE_URL+endpoint, headers=headers)