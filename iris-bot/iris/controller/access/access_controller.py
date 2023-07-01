from slack_bolt import App
import service.access.access_service as service
from service.main_service import close_message

def load_commands(app:App):

    @app.command("/acessos")
    def show_request_message(body, ack, client):
        ack()

        service.send_request_message(body, client)

    @app.action("select_tool")
    def update_message(ack, body, client):

        service.select_tool(ack, body, client)

    @app.action("access_select_department")
    def update_message(ack, body, client):

        service.select_department(ack, body, client)

    @app.action("button_access_confirmar")
    def confirmar(ack, body, client):
        ack()
        message = "Solicitação enviada :white_check_mark:"
        close_message(ack,body, client,message)
        service.send_request_message_to_manager(ack, body, client)

    @app.action("button_access_aprovar")
    def confirmar(ack, body, client):
        ack()
        
        approved = True
        
        close_message(ack,body,client,":white_check_mark: Você aprovou este acesso!")
        service.send_request_approve_message(ack,body,client,approved)
        

    @app.action("button_access_negar")
    def negar(ack, body, client):
        ack()

        approved = False

        service.send_request_approve_message(ack,body,client,approved)
        close_message(ack,body,client,":x: Você negou este acesso!")
