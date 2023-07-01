from repository.github_repository import user_is_organization_member, team_exists
import util.block_mounter as block_mounter

def insert_username(ack,body, client):
    ack()
        
    github_user = body['actions'][0]['value']

    channel_id = body['container']['channel_id']
    action_ts = body['message']['ts']

    if(user_is_organization_member(github_user) == False):
        blocks = [block_mounter.mount_text("Opa, pelo que eu vi aqui seu usuário ainda não está incluído na nossa organização, favor abrir um chamado para o time de GAC para a inclusão do seu e-mail ao AD da Linx\n<https://jira.linx.com.br/secure/RapidBoard.jspa?rapidView=4137&projectKey=DICLD&view=detail&selectedIssue=DICLD-8750|Clique aqui para ser redirecionado para o quadro>")]
        
    else:
        blocks = body['message']['blocks']
        blocks[3] = block_mounter.mount_text(f"*Usuário:*\n\t{github_user}")
        blocks.append(block_mounter.mount_input("Insira o nome do time", "plain_text_input", "input_team"))

    client.chat_update(channel = channel_id, ts=action_ts, blocks=blocks)

def insert_team (ack,body, client):
    ack()

    blocks = body['message']['blocks']
    
    channel_id = body['container']['channel_id']
    action_ts = body['message']['ts']

    team_name = body['actions'][0]['value']
    
    team_name = team_name.replace(" ","-")
    
    
    if(team_exists(team_name) == False):
        blocks = (block_mounter.mount_text(f"Não encontrei o time {team_name} na organização Chaordic :(. Verifique se o time inserido está correto e abra uma nova solicitação"),)
    else :
        blocks[4] = block_mounter.mount_text(f"*Time*:\n\t{team_name}")
        block_mounter.append_confirmation_block(blocks)
    client.chat_update(channel = channel_id, ts=action_ts, blocks=blocks)
        