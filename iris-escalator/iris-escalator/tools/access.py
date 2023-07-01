
def mount_message(message:str):
    return lambda *parameters : message.format(*parameters)

TOOLS = {
    "Github":{
        "image":"https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
        'message': mount_message("o nome de usuário do solicitante é {} e será incluido no time {}.\nOBS: Serão liberados também todos os repositórios ligados ao time solicitado"),
        'db_columns': ('github_user','github_team',),
        'used_db_columns': ('requester_uid',)
    },
    "VPN":{
        'image':'https://pritunl.com/img/logo.png',
        'message': mount_message("este usuário será incluído no grupo {}"),
        'db_columns': ('vpn_organization',),
        'used_db_columns': ('requester_uid','requester_mail',)
    }
}