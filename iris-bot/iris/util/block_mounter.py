def mount_text(text:str):
	return ({
			"type": "section",
			"text": {
				"type": "mrkdwn",
				"text": text
			}
		})
	

def mount_select(label, options, action_id, _type="static_select"):

	return ({
			"type": "input",
		    "element": {
				"type": _type,
			    "options": [{
					"text": {
							"type":"plain_text",
							"text": option if type(option) is str else option['name']
						},
						"value": option if type(option) is str else option['value']
					} for option in options],
			    "action_id": action_id
		    },
		    "label": {
			    "type": "plain_text",
			    "text": label
		    }
		})

def mount_input(label:str, _type:str, action_id:str):
	return ({
			"dispatch_action": True,
			"type": "input",
			"element": {
				"type": _type,
				"action_id": action_id
			},
			"label": {
				"type": "plain_text",
				"text": label
			}
		})

def mount_buttons(buttons:list[dict]):
	return ({
			"type": "actions",
			"elements": [{
				"type": "button",
				"text": {
					"type":"plain_text",
					"text":button['text']
				},
				"style": button['style'],
				"value": button.get('value', button['text']),
				'action_id': button['action_id']
			} for button in buttons]
		})

def mount_approve_access_message(user:str, message:str, tool:str, converted_time:str, img:str, id_request:int):

	blocks = (
		mount_text(f"Olá, tudo bem? Chegou para você uma nova solicitação de acesso do usuário <@{user}> na ferramenta *{tool}*, {message}"),
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
		mount_buttons(
			[
				{
					"text":"Approvar",
					"style": "primary",
					"action_id": "button_access_aprovar",
					"value": str(id_request)
				},
				{
					"text":"Negar",
					"style": "danger",
					"action_id": "button_access_negar",
					"value": str(id_request)
				}
			]
		))

	return blocks

def append_confirmation_block(blocks:list):
	blocks.append(mount_text("Agora só falta mais um passo! Confirme se as informações acima estão corretas!\nSe estiver tudo certo, clique em *Confirmar* para a sua solicitação de acesso ser encaminhada para o seu gestor responsável"))

	blocks.append(mount_buttons([
	    {
            'text':'Confirmar',
            'style':'primary',
            'action_id':'button_access_confirmar'
        },
        {
            'text':'Cancelar',
            'style':'danger',
            'action_id':'button_cancelar'
        }
    ]))