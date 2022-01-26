import datetime
from slack_bolt import App
from dateutil import relativedelta
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


@app.command("/kitchenday")
def handle_kitchenday(ack, body, logger):
    ack()

    values = getSheetValues("Kitchen!A1:B15")
    totalAmount = len(values)
    print(totalAmount)    


    myI = list(map(lambda x: x[1], values)).index(body["user_id"])


    if myI == -1:
        messageEphemeral("You are not on the kitchen day list", body["user_id"], title="Kitchenday!")
        return
        
    datetime.date(year=2021, month=12, day=18)
    delta = relativedelta.relativedelta(datetime.date.today(), datetime.date(year=2021, month=12, day=18))
    remDelta = (myI - delta.days) % 12

    if remDelta != 0:

        sTag = "" if remDelta == 1 else "s"
        nextDay = datetime.date.today() + datetime.timedelta(days=remDelta)
        nextDayString = nextDay.strftime("%A, %B %d")
        message = f"Your next kitchen day is in {remDelta} day{sTag} (on {nextDayString}).\n\n"

        today = delta.days % 12
        message += "It is {}'s kitchen day.\n".format(values[today][0])

        messageEphemeral(message, body, title="Kitchenday!")
    else:
        messageEphemeral("It is your kitchen day!\n", body, title="Kitchenday!")


# Start your app
if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()