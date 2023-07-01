from api.jenkins_api import base_request

def execute_access_job(tool:str, parameters:str):
    print(f"Grant access on {tool} with {parameters}")
    base_request(f"/job/CORE-Grant{tool}Access/buildWithParameters?{parameters}")
    