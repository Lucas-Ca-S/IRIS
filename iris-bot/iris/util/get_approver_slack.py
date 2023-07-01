import os

environment = os.environ.get("DEV_ENVINROMENT", None)

def get_approver_slack(client, slack_user_email, manager_mail):
    if(environment):
        return client.users_lookupByEmail(email=slack_user_email)
    
    return client.users_lookupByEmail(email=manager_mail)