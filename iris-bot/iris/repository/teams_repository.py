from api.teams_api import base_request

def get_user_manager(user_email:str):
    return base_request("/users/"+user_email+"/manager").json()

def get_manager_email(user_mail:str):
    return get_user_manager(user_mail)['mail']

def get_manager_display_name(user_mail:str):
    return get_user_manager(user_mail)['displayName']