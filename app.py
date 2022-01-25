from slack_bolt import App

from slack_bolt.adapter.socket_mode import SocketModeHandler
from sheets import *
from constants import *
from helpers import *


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

            messageEphemeral(app, text, body, title="Dues")



# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()