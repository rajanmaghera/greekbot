from constants import *

def messageEphemeral(app, text, body, title=BOT_TITLE):

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

def messageTreasurer(app, message):
    app.client.chat_postMessage(
        # as_user=False,
        channel=TREASURER_USER_ID,
        text=message
    )

def messageUser(app, message, user):
    app.client.chat_postMessage(
        channel=user,
        text=message,
    )

