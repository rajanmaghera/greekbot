from dotenv import load_dotenv
from os import environ

load_dotenv()
SLACK_BOT_TOKEN = environ.get("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = environ.get("SLACK_APP_TOKEN")
PAYMENT_MESSAGE = environ.get("PAYMENT_MESSAGE")
TREASURER_USER_ID = environ.get("TREASURER_USER_ID")
BOT_TITLE = environ.get("BOT_TITLE")
# The ID of a sample document.
DOCUMENT_ID = environ.get("DOCUMENT_ID")