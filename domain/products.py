import domain.database as database

COLLECTION = 'products'
DATABASE_CONNECTION = database.get_database()


def get_products():
    return DATABASE_CONNECTION[COLLECTION].find()


def get_product(id):
    return DATABASE_CONNECTION[COLLECTION].find_one({"_id": id})


def add_product(product):
    DATABASE_CONNECTION[COLLECTION].replace_one({'_id': product['_id']}, product, upsert=True)


def populate_products():
    products = [
        {
            "_id": "6e3777b7-f6d4-401c-ada2-18283d6ece40",
            "name": "Великий м'ясний бургер",
            "price": 149.99,
            "url": "https://insanelygoodrecipes.com/wp-content/uploads/2020/05/Burger-with-fries-1024x536.png"
        },
        {
            "_id": "791fc74b-6b15-4edb-a8f2-5263113891cb",
            "name": "Кока-кола 0.5",
            "price": 29.99,
            "url": "https://cooker.net.ua/upload/iblock/4c5/bezalkogolniy-napiy-coca-cola-0-5l-720_preview.jpg"
        }
    ]

    for product in products:
        add_product(product)
