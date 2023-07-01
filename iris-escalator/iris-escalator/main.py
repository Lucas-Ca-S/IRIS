from database.database import Database
from slack_sdk import WebClient
from datetime import datetime
from tools.access import TOOLS
from repository.teams_repository import get_manager_display_name
import os, block_mounter, pytz

SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=SLACK_BOT_TOKEN)

database_access = Database("access_requests")

requests = database_access.select("request_id, requester_uid, thread_ts, requested_tool, request_date, approver_mail, escalated_approver_mail, escalated", "approved_by IS NULL AND denied_by IS NULL AND DATE(request_date) <= NOW() - INTERVAL 3 DAY")

print(requests)

for request in requests:
    (request_id, requester_uid, thread_ts, requested_tool, request_date, approver_mail, escalated_approver_mail, escalated) = request

    if escalated:
        manager_slack = client.users_lookupByEmail(email=escalated_approver_mail)
     
        #Resgatando valores do chat do gestor para enviar a mensagem
        conversation = client.conversations_open(users=manager_slack['user']['id'])
        chanel_id = conversation['channel']['id']

        blocks = (block_mounter.mount_text(f"Opa! O usuário <@{requester_uid}> tinha aberto uma solicitação de acesso na ferramenta *{requested_tool}*, porém o gestor direto do solicitante não aprovou no prazo de 3 dias úteis, então escalei a solicitação para você, porém no dia seguinte depois do escalamento, ainda não houve aprovação da solicitação, portanto irei encerrar a solicitação.\n"),)

        client.chat_update(channel=chanel_id, ts=thread_ts, blocks=blocks)

        conversation = client.conversations_open(users=requester_uid)
        chanel_id = conversation['channel']['id']

        blocks = (block_mounter.mount_text(f"Olá! Infelizmente a sua solicitação de acesso na ferramenta *{requested_tool}* não foi aprovada por ninguém no prazo de 4 dias, por isso irei encerra-la, mas não se preocupe, você pode solicitar novamente o acesso e pedir para sua gestão aprovar o mesmo."),)

        result = client.chat_postMessage(channel=chanel_id, blocks= blocks)

        database_access.update("denied_by = 'IRIS', denial_date = NOW()", request_id)
    else:
        manager_slack = client.users_lookupByEmail(email=approver_mail)
        
        conversation = client.conversations_open(users=manager_slack['user']['id'])
        chanel_id = conversation['channel']['id']

        escalated_manager_display_name = get_manager_display_name(approver_mail)

        blocks = (block_mounter.mount_text(f"Opa! O usuário <@{requester_uid}> tinha aberto uma solicitação de acesso na ferramenta *{requested_tool}* que foi encaminhada a você, porém devido a falta de interação em 3 dias úteis depois da abertura da solicitação, estarei fechando a solicitação aqui, mas não se preocupe, eu sei como vida de gestor é ocupada(ou talvez você esteja de férias), então escalei essa solicitação para {escalated_manager_display_name}"), )
        
        client.chat_update(channel=chanel_id, ts=thread_ts, blocks=blocks)

        tool_db_columns = TOOLS[requested_tool]['db_columns']

        tool_db_columns_values = database_access.select_one(','.join(tool_db_columns), "request_id = %s", request_id)

        message = TOOLS[requested_tool]['message'](*tool_db_columns_values)
            
        img = TOOLS[requested_tool]['image']

        IST = pytz.timezone('Brazil/East')
        datetime_utc = datetime.now(IST)
        converted_time = datetime_utc.strftime('%d/%m/%Y %H:%M:%S')

        blocks = block_mounter.mount_approve_access_message(manager_slack['user']['id'], requester_uid, requested_tool, message, converted_time, img, request_id)

        escalated_manager_slack = client.users_lookupByEmail(email=escalated_approver_mail)

        escalated_manager_uid = escalated_manager_slack['user']['id']

        #Resgatando valores do chat do gestor para enviar a mensagem
        conversation = client.conversations_open(users=escalated_manager_uid)
        chanel_id = conversation['channel']['id']

        result = client.chat_postMessage(channel=chanel_id, blocks=blocks)
        
        database_access.update("escalated = 1, thread_ts = %s", result['message']['ts'], request_id)

        conversation = client.conversations_open(users=requester_uid)
        chanel_id = conversation['channel']['id']

        blocks = (block_mounter.mount_text(f"Olá de novo!\nO seu gestor não aprovou a sua solicitação de acesso na ferramenta *{requested_tool}* no prazo, mas não se preocupe, eu escalei a sua solicitação para o <@{escalated_manager_uid}>"),)

        client.chat_postMessage(channel=chanel_id, blocks=blocks)
