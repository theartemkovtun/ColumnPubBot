TOKEN = "5035420243:AAH7J-tx7jouOdNnXri2RkrJuXopjLq4N_0"

PROJECT_NAME = 'column-pub-bot'

WEBHOOK_HOST = f"https://{PROJECT_NAME}.herokuapp.com"
WEBHOOK_PATH = '/webhook/' + TOKEN
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

MONGO_CONNECTION_STRING = 'mongodb+srv://Vova:Vova@cluster0.nen71.mongodb.net/Claster0?retryWrites=true&w=majority'
MONGO_DB_NAME = 'columnpubbotdb'