import domain.database as database

COLLECTION = 'users'
DATABASE_CONNECTION = database.get_database()


def add_user(user):
    DATABASE_CONNECTION[COLLECTION].replace_one({'_id': user['_id']}, user, upsert=True)
