from repository.vpn_repository import user_is_organization_member
import util.block_mounter as block_mounter

def select_group(ack,body, client):
    ack()

    user_id= body['user']['id']
    user_email=client.users_info(user=user_id)['user']['profile']['email']
        
    group = body['actions'][0]['selected_option']['text']['text']
    group_id = body['actions'][0]['selected_option']['value']

    channel_id = body['container']['channel_id']
    action_ts = body['message']['ts']

    if(user_is_organization_member(group_id, user_email)):
        blocks = (block_mounter.mount_text(f"⁉️Opa, pelo que eu vi aqui seu usuário já está incluído na organização *{group}*."),)
        
    else:
        blocks = body['message']['blocks']
        blocks[3] = block_mounter.mount_text(f"*Grupo:*\n\t{group}")
        block_mounter.append_confirmation_block(blocks)

    client.chat_update(channel = channel_id, ts=action_ts, blocks=blocks)