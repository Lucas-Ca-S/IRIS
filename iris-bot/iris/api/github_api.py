from requests import post, request
import os

API_SECRET = os.environ['GITHUB_API_SECRET']

BASE_URL = "https://api.github.com"
GRAPHQL_URL = "https://api.github.com/graphql"

HEADERS = {
    'Accept':'application/vnd.github+json',
    'Authorization':f'Bearer {API_SECRET}'
}

def base_request(endpoint:str):
    return request(url=BASE_URL+endpoint, headers=HEADERS, method="GET")

def base_request_graph(query:str):
    return post(url=GRAPHQL_URL, headers=HEADERS, json={'query': query})