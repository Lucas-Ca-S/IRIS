import util.block_mounter as block_mounter, pytz
from datetime import datetime
from tools.access import TOOLS
from repository.teams_repository import get_user_manager
import repository.jenkins_repository as jenkins
from database.database import Database
from util.get_approver_slack import get_approver_slack
from service.main_service import show_manager

database_access = Database("access_requests")

def send_request_message(body, client):
    
    user_id = body['user_id']
    conversation = client.conversations_open(users=user_id)
    chanel_id = conversation['channel']['id']
    
    user_info=client.users_info(user=user_id)
    user_first_name=user_info['user']['profile']['first_name']
    blocks = (
        block_mounter.mount_text(f"Olá {user_first_name}!  Eu sou a _*Iris*_, o serviço de gestão de acesso para ferramentas internas da Linx Digital, e estou aqui para ajudá-lo a solicitar as ferramentas que você precisa para ser um verdadeiro pro! :robot_face:\n\n\nMas antes de começarmos, eu gostaria de lembrá-lo que preciso das informações necessárias para processar sua solicitação. Não se preocupe, eu não vou pedir para você dançar ou cantar, apenas algumas informações importantes, ok?"),
        block_mounter.mount_select("Então para começarmos, por favor informe o departamento ao qual você pertence", TOOLS.keys(), 'access_select_department')
        )
    client.chat_postMessage(channel=chanel_id, blocks= blocks)

def select_department(ack, body, client):
    ack()

    channel_id = body['container']['channel_id']
    action_ts = body['message']['ts']

    selected_product = body['actions'][0]['selected_option']['text']['text']

    blocks = body['message']['blocks']

    action_id = "select_tool"

    blocks[1] = block_mounter.mount_text(f"*Departamento:*\n\t{selected_product}")

    options = TOOLS[selected_product].keys()

    blocks.append(block_mounter.mount_select("Muito bem! Agora vamos selecionar a ferramenta", options,action_id))

    client.chat_update(channel = channel_id, ts=action_ts, blocks=blocks)

def select_tool(ack, body, client):
    ack()
    
    channel_id = body['container']['channel_id']
    action_ts = body['message']['ts']

    blocks = body['message']['blocks']

    selected_tool = body['actions'][0]['selected_option']['text']['text']
        
    selected_product = blocks[1]['text']['text'].split("\n\t")[1]
 
    tool = TOOLS[selected_product][selected_tool]
    parameter = tool['initial_parameters']

    blocks[2] = block_mounter.mount_text(f"*Ferramenta:*\n\t{selected_tool}")

    blocks.append(parameter.mount_first_parameter())

    client.chat_update(channel = channel_id, ts=action_ts, blocks=blocks)

def send_request_message_to_manager(ack,body, client):
    ack()
    
    #Resgatando info do usuário que solicitou o acesso
    user_info=client.users_info(user=body['user']['id'])
    slack_user_email = user_info['user']['profile']['email']
    
    #Enviar a solicitação pro gestor
    manager = get_user_manager(slack_user_email)
    manager_mail = manager['mail']

    escalated_manager = get_user_manager(manager_mail)
    escalated_manager_mail = escalated_manager['mail']
    
    channel_id = body['container']['channel_id']
    show_manager(channel_id, manager['displayName'], escalated_manager['displayName'], client)

    #Definindo variaveis para montar o bloco da mensagem pro gestor
    blocks = body['message']['blocks']
    product = blocks[1]['text']['text'].split("\n\t")[1]
    tool = blocks[2]['text']['text'].split("\n\t")[1]

    parameters = [block['text']['text'].split("\n\t")[1] for block in blocks[3:-2]]
    
    username = body['user']['username']
    IST = pytz.timezone('Brazil/East')
    datetime_utc = datetime.now(IST)
    converted_time = datetime_utc.strftime('%d/%m/%Y %H:%M:%S')

    img = TOOLS[product][tool]['image']

    #Resgatando valores do chat do gestor para enviar a mensagem
    manager_slack = get_approver_slack(client, slack_user_email, manager_mail)
    conversation = client.conversations_open(users=manager_slack['user']['id'])
    channel_id = conversation['channel']['id']

    db_columns = TOOLS[product][tool]['db_columns']

    new_request_id = database_access.insert(f"requester_mail, product, requester_uid, requested_tool, approver_mail, escalated_approver_mail, {','.join(db_columns)}", slack_user_email, product, body['user']['id'], tool, manager_mail, escalated_manager_mail, *parameters)
   
    blocks = block_mounter.mount_approve_access_message(username, TOOLS[product][tool]['message'](*parameters), tool, converted_time, img, new_request_id)

    result = client.chat_postMessage(channel=channel_id, blocks= blocks)

    database_access.update("thread_ts = %s", result['message']['ts'], new_request_id)

def send_request_approve_message(ack, body, client,approved):
    ack()

    request_id = body['actions'][0]['value']

    user_info=client.users_info(user=body['user']['id'])
    responder_mail = user_info['user']['profile']['email']
    
    manager_id = body['user']['id']

    (user_uid, product, tool) = database_access.select_one("requester_uid, product, requested_tool", "request_id = %s", request_id)
    conversation = client.conversations_open(users=user_uid)
    chanel_id = conversation.get('channel')['id']
    
    if(approved):
        
        db_columns = TOOLS[product][tool]['db_columns']+TOOLS[product][tool]['used_db_columns']

        parameters_values = database_access.select_one(','.join(db_columns), "request_id = %s", request_id)
        
        parameters = '&'.join(f"{k}={v}" for k, v in zip(db_columns, parameters_values))
        jenkins.execute_access_job(tool, parameters)
    
        message = f"""
Olá novamente, Iris aqui para dar uma ótima notícia! O acesso que você solicitou à nossa ferramenta foi aprovado pelo gestor(a) superpoderoso(a) <@{manager_id}>! Agora vou executar as tarefas necessárias para liberar seu acesso e em breve você estará livre para navegar e utilizar a ferramenta solicitada. 👨‍💻👩‍💻

        
Se você tiver alguma dúvida, nossa equipe de Cloud-Digital está aqui para ajudar! Basta falar com a gente. Ah, e se precisar de algum outro acesso, é só me chamar novamente! 😉👍

        
Tenham um ótimo dia e aproveite a ferramenta! 🎉

        
Abraços,
Iris🤖
        """
        column = "approved_by"
        date_column = "approval_date"
    else:
        message = f"""
Olá de novo, humano! Iris na área com uma notícia que talvez não seja tão legal assim... 🙁 Infelizmente, o gestor(a) <@{manager_id}>, decidiu negar o seu pedido.

        
Caso tenha alguma dúvida sobre a decisão, por favor entre em contato diretamente com o seu gestor. E se por acaso encontrar algum erro estranho sobre mim, não hesite em falar com o time de Cloud-Digital - nós sempre estamos melhorando!


Agora é hora de seguir em frente e continuar trabalhando duro, porque a vida não para! Qualquer outra necessidade que tiver, pode contar comigo.


Abraços,
Iris 🤖
        """
        column = "denied_by"
        date_column = "denial_date"

    database_access.update(f"{column} = %s, {date_column} = NOW()", responder_mail, request_id)
    blocks = (block_mounter.mount_text(message),)
    client.chat_postMessage(channel=chanel_id, blocks=blocks)