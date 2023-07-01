from api.github_api import base_request, base_request_graph

ORG_URL = "/orgs/chaordic"

def user_is_organization_member(user:str):

    return base_request(f"{ORG_URL}/members/{user}").status_code == 204

def team_exists(team_name:str):
    return base_request(f"{ORG_URL}/teams/{team_name}").status_code == 200

def user_is_team_member(team:str, user:str):
    return base_request(f"{ORG_URL}/teams/{team}/memberships/{user}").status_code == 200

def get_user_teams(user:str):

    querry = 'query { organization(login: "chaordic") {teams(first: 30,userLogins: ["'+user+'"]) {nodes {name,slug}}}}'

    result = base_request_graph(querry).json()
   
    nodes = result['data']['organization']['teams']['nodes']

    return [{'name':node['name'], 'value':node['slug']} for node in nodes]

def repository_exists(repository_name:str):
    return base_request(f"/repos/chaordic/{repository_name}").status_code == 200