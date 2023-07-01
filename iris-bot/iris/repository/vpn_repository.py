from api.vpn_api import base_request

def user_is_organization_member(organization_id:str, user_search:str):
    response_json = base_request(f"/user/{organization_id}").json()

    index_bottom = 0
    index_top = len(response_json)-1
    while (index_bottom<=index_top):
        
        middle = int((index_bottom+index_top)/2)

        user = response_json[middle]['name']

        if(user == user_search):
            return True
        
        if(user_search<user):
            index_top = middle - 1
        else:
            index_bottom = middle + 1

    return False