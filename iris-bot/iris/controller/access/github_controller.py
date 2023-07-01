from slack_bolt import App
import service.access.github_service as service

def load_commands(app:App):
    @app.action("start_github")
    def insert_username(ack,body, client):
        
        service.insert_username(ack,body, client)

    @app.action("input_team")
    def insert_team(ack,body, client):

        service.insert_team(ack,body, client)