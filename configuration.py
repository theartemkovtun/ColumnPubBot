TOKEN = ""

PROJECT_NAME = 'column-pub-bot'

WEBHOOK_HOST = f"https://{PROJECT_NAME}.herokuapp.com"
WEBHOOK_PATH = '/webhook/' + TOKEN
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

MONGO_CONNECTION_STRING = 'mongodb://localhost'
MONGO_DB_NAME = 'columnpubbotdb'