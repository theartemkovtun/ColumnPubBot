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


def add_admin():
    user = {
        "_id": "59d05d65-b787-42f1-a212-6fc42a9ea057",
        "role": "1",
        "chat_id": 387186275,
        "fullname": "Test admin user",
        '_address': ''
    }
    DATABASE_CONNECTION[COLLECTION].replace_one({'_id': user['_id']}, user, upsert=True)


def check_if_user_admin(chat_id):
    user = USERS.find_one({'chat_id': chat_id})
    return user is not None and user['role'] == "1"
