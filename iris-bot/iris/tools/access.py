from .vpn_groups import get_vpn_groups
from .first_parameter import InputInitParameter, SelectInitParameter, MultiSelectInitParameter

def mount_message(message:str):
    return lambda *parameters : message.format(*parameters)

def get_tools_product():
    rh_tools = {
        'Em construção...:building_construction:':{
            'id' : 'id_tool',
            'image':'link_image_here',
            'initial_parameters':{
                'param1': 'value1',
                'param2': 'value2',
            },
        }
    }
    rh_tools.update(get_general_tools('RH'))
    
    development_tools = {
        'Jenkins': {
            'image':'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Jenkins_logo.svg/1200px-Jenkins_logo.svg.png',
            'initial_parameters': SelectInitParameter('Selecione o job', "start_jenkins",
                                                        ['CORE-ApplicationPool', 'CORE-CreateCertificate',
                                                        'CORE-PurgeRedis', 'CORE-RestaurarAmbienteProva',
                                                        'CORE-StartDEV-VMs', 'CORE-TasksFarm', 'LinxIO-SwitchEnvironment(Admin)']),
            'message': mount_message("o solicitante terá os grupos de permissões {}"),
            'db_columns': ('ad_team',),
            'used_db_columns': ('requester_uid', 'requester_mail')
        },
        'MySQL': {
            'image':'https://upload.wikimedia.org/wikipedia/commons/thumb/e/e9/Jenkins_logo.svg/1200px-Jenkins_logo.svg.png',
            'initial_parameters': MultiSelectInitParameter('Selecione os jobs', "start_jenkins",
                                                    ['CORE-ApplicationPool', 'CORE-CreateCertificate',
                                                        'CORE-PurgeRedis', 'CORE-RestaurarAmbienteProva',
                                                        'CORE-StartDEV-VMs', 'CORE-TasksFarm', 'LinxIO-SwitchEnvironment(Admin)']),
            'message': mount_message("o solicitante terá os grupos de permissões {}"),
            'db_columns': ('ad_team',),
            'used_db_columns': ('requester_uid', 'requester_mail')
        },
    }
    development_tools.update(get_general_tools('Desenvolvimento'))
    
    qa_tools = {
        'Em construção...:building_construction:':{
            'id' : 'id_tool',
            'image':'link_image_here',
            'initial_parameters':{
                'param1': 'value1',
                'param2': 'value2',
            },
        }
    }
    qa_tools.update(get_general_tools('QA'))
    
    return {
        'RH': rh_tools,
        'Desenvolvimento': development_tools,
        'QA': qa_tools,
    }

def get_general_tools(department:str):
    return {
        'Github': {
            'image':'https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png',
            'initial_parameters': InputInitParameter('plain_text_input', 'Insira o seu usuário do Github', "start_github"),
            'message': mount_message("o nome de usuário do solicitante é {} e será incluido no time {}.\nOBS: Serão liberados também todos os repositórios ligados ao time solicitado"),
            'db_columns': ('github_user','github_team',),
            'used_db_columns': ('requester_uid',)
        },
        'VPN': {
            'id' : 'start_vpn',
            'image':'https://pritunl.com/img/logo.png',
            'initial_parameters': SelectInitParameter("Selecione o grupo da VPN", "start_vpn", get_vpn_groups(department)),
            'message': mount_message("este usuário será incluído no grupo {}"),
            'db_columns': ('vpn_organization',),
            'used_db_columns': ('requester_uid','requester_mail',)
        }
    }

TOOLS = get_tools_product()