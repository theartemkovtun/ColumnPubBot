import domain.database as database

COLLECTION = 'users'
DATABASE_CONNECTION = database.get_database()
USERS = DATABASE_CONNECTION[COLLECTION]


def add_user(user):
    DATABASE_CONNECTION[COLLECTION].replace_one({'_id': user['_id']}, user, upsert=True)


def get_user(chat_id):
    return USERS.find_one({'chat_id': chat_id})


def check_user_has_address(_id):
    user = USERS.find_one({'_id': _id})
    address = user['_address']
    return not address
