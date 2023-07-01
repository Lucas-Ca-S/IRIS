from slack_bolt import App
import service.main_service as service

def load_commands(app:App):

    @app.action("button_cancelar")
    def confirmar(ack, body, client):
        ack()

        message= "Solicitação cancelada :exclamation:"

        service.close_message(ack,body, client, message)
