from dotenv import load_dotenv
load_dotenv()

import controller.start_bot as bot

if __name__ == "__main__":
    bot.start()
