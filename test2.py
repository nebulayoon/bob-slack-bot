import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from flask import Flask, request

from dotenv import load_dotenv

load_dotenv(verbose=True)
BOT_TOKEN = os.getenv("BOT_TOKEN")
APP_TOKEN = os.getenv("APP_TOKEN")

app = App(token=BOT_TOKEN)


@app.event("app_mention")
def who_am_i(event, client, message, say):
    print("event:", event)
    print("client:", client)
    print("message:", message)

    say(f'안녕하세요! 밥입니다! <@{event["user"]}>')


flask_app = Flask(__name__)

# SlackRequestHandler translates WSGI requests to Bolt's interface
# and builds WSGI response from Bolt's response.
from slack_bolt.adapter.flask import SlackRequestHandler

handler = SlackRequestHandler(app)


# Register routes to Flask app
@flask_app.route("/slack/events", methods=["POST"])
def slack_events():
    # handler runs App's dispatch method
    return handler.handle(request)


if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=3000)
