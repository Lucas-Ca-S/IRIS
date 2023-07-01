from requests import request
import os

CREDENTIALS = os.environ['JENKINS_CREDENTIALS']
HOST = os.environ['JENKINS_HOST']

BASE_URL = f"http://{CREDENTIALS}@{HOST}:8080"

def base_request(endpoint:str):
    return request("POST", BASE_URL+endpoint)