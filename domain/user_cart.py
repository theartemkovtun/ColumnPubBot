import domain.database as database

COLLECTION = 'cart'
DATABASE_CONNECTION = database.get_database()


def save_user_cart(cart):
    DATABASE_CONNECTION[COLLECTION].replace_one({'_id': cart['_id']}, cart, upsert=True)


def get_user_cart(chat_id):
    return DATABASE_CONNECTION[COLLECTION].find_one({"chat_id": chat_id})


def delete_user_cart(chat_id):
    return DATABASE_CONNECTION[COLLECTION].delete_one({"chat_id": chat_id})

