import domain.database as database

COLLECTION = 'feedback'
DATABASE_CONNECTION = database.get_database()
FEEDBACK = DATABASE_CONNECTION[COLLECTION]


def add_feedback(feedback):
    FEEDBACK.replace_one({'_id': feedback['_id']}, feedback, upsert=True)


