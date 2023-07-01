def mount_text(text:str):
	return (
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": text
			}
		}
	)

def mount_buttons(buttons:list[dict]):
	return (
		{
			"type": "actions",
			"elements": list(map(lambda button: {
				"type": "button",
				"text": {
					"type":"plain_text",
					"text":button['text']
				},
				"style": button['style'],
				"value": button.get('value', button['text']),
				'action_id': button['action_id']
			}, buttons))
		}
	)

def mount_approve_access_message(manager_uid:str, user_uid:str, tool:str, message:str, converted_time:str, img:str, id_request:int):
	blocks = (
		mount_text(f"Olá, tudo bem? Vim aqui com uma solicitação de acesso do usuário <@{user_uid}> na ferramenta *{tool}*, {message}.\n*OBS*:Esta solicitação de acesso era destinado ao gestor do solicitante informado <@{manager_uid}>, porém ele/ela não aprovou a solicitação dentro do prazo de 3 dias úteis, então decidi escalar a solicitação para você."),
		{
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": f"*Data e hora da solicitação:*\n\t{converted_time}"
			},
			"accessory": {
				"type": "image",
				"image_url": img,
				"alt_text": "computer thumbnail"
			}
		},
		mount_text("Valide com carinho as informações acima, se estiver tudo certo, clique em *Aprovar* para liberar o acesso na ferramenta solicitada para o usuário"),
		mount_buttons([
		{
			"text":"Approvar",
			"style": "primary",
			"action_id": "button_aprovar",
			"value": str(id_request)
		},
		{
			"text":"Negar",
			"style": "danger",
			"action_id": "button_negar",
			"value": str(id_request)
		}
	]))

	return blocks
