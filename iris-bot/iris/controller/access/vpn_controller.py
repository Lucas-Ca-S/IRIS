from slack_bolt import app
import service.access.vpn_service as service

def load_commands(app:app):
    @app.action("start_vpn")
    def select_group(ack,body, client):
        
        service.select_group(ack,body, client)