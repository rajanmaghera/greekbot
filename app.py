from slack_bolt import App
from dotenv import load_dotenv
from slack_bolt.adapter.socket_mode import SocketModeHandler
import os

load_dotenv()
SLACK_BOT_TOKEN = os.environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.environ.get("SLACK_APP_TOKEN")
PAYMENT_MESSAGE = os.environ.get("PAYMENT_MESSAGE")
BOT_TITLE = os.environ.get("BOT_TITLE")

# Initializes your app with your bot token and socket mode handler
app = App(token=SLACK_BOT_TOKEN)



@app.command("/dues")
def handle_dues(ack, body, logger):
    ack()

    values = getSheetValues("Sheet1!A2:G120")
    for row in values:
        if row[1] == body["user_id"]:

            text = f"You owe ${row[3]} in dues. {PAYMENT_MESSAGE} If you have any questions, please contact the Treasurer."

            if int(row[3]) <= 0:
                text = f"You do not owe any dues for this semester."

            messageEphemeral(text, body, title="Dues")

def messageEphemeral(text, body, title=BOT_TITLE):

    conversations = app.client.conversations_list()["channels"]
    if body["channel_id"] in list(map(lambda x: x["id"], conversations)):

        app.client.chat_postEphemeral(
            channel=body["channel_id"],
            user=body["user_id"],
            text=f"{text}"
        )
    else:
        app.client.views_open(
            trigger_id=body["trigger_id"],
            view={
                "type": "modal",
                "title": {
                    "type": "plain_text",
                    "text": f"{title}",
                    "emoji": True
                },
                "close": {
                    "type": "plain_text",
                    "text": "Close",
                    "emoji": True
                },
                "blocks": [
                    {
                        "type": "section",
                        "text": {
                            "type": "plain_text",
                            "text": f"{text}",
                            "emoji": True
                        }
                    }
                ]
            }
        )

# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()