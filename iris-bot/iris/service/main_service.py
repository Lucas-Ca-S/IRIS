import util.block_mounter as block_mounter

def close_message(ack, body, client, message):
    ack()
    
    channel_id = body['container']['channel_id']
    action_ts = body['message']['ts']

    blocks = body['message']['blocks']

    last_block_index = len(blocks)-1

    blocks[last_block_index] = block_mounter.mount_text(message)
    
    client.chat_update(channel = channel_id, ts=action_ts, blocks=blocks)

def show_manager(conversation_id:str, manager_display_name:str, escalated_manager_display_name:str, client):

    blocks =  [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"Bom... Com base na organização do Teams, identifiquei o(a) seu gerente atual seria o(a) {manager_display_name} e gostaria de informar que a sua solicitação foi enviada para análise.\n\n\nAgora é só esperar a resposta do(a) gerente e caso o seu gestor atual não aprove em 3 dias irei escalar a sua solicitação de acesso para o {escalated_manager_display_name}, enquanto isso, nada de querer acessar as ferramentas sem a devida autorização, hein! Eu tô de olho!:eyes: \n\n\nRelaxa que vou ficar de olho na sua solicitação e assim que tiver uma resposta do(a) gerente, volto aqui pra te dar o feedback. Ah, e não se esqueça de enviar uma caixinha de biscoitos pra mim quando você conseguir o acesso, hein!"
            }
        }
    ]
        
    client.chat_postMessage(channel=conversation_id, blocks= blocks)   
