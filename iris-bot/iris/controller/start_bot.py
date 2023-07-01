from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os, controller.main_controller as main_controller, controller.access.access_controller as access_controller,  controller.access.github_controller as github_controller, controller.access.vpn_controller as vpn_controller

SLACK_APP_TOKEN = os.environ["SLACK_APP_TOKEN"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]

app = App(token=SLACK_BOT_TOKEN)

def start():
    access_controller.load_commands(app)
    main_controller.load_commands(app)
    github_controller.load_commands(app)
    vpn_controller.load_commands(app)
    
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()
