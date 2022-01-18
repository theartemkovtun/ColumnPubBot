from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import configuration
import os
from domain import products, users, user_cart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import messages
from keyboards.menu_item import item_cb, menu_item_markup
from keyboards.cart_item import cart_cb, cart_item_markup
from functools import reduce
import uuid

bot = Bot(token=configuration.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    users.add_user({
        "_id": str(uuid.uuid4()),
        "chat_id": message.chat.id,
        "fullname": message.chat.full_name
    })

    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(messages.menu)
    markup.add(messages.contact_us)
    markup.add(messages.cart)

    await message.answer(f'{message.chat.first_name}, '
                         f'Ласкаво просимо до ColumnPub чат боту. Дякуємо, що обрали наш ресторан', reply_markup=markup)


@dp.message_handler(text=messages.back_to_home)
async def cmd_menu(message: types.Message):
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(messages.menu)
    markup.add(messages.contact_us)
    markup.add(messages.cart)

    await message.answer('Головна сторінка', reply_markup=markup)

@dp.message_handler(text=messages.menu)
async def cmd_menu(message: types.Message):
    all_items = products.get_products()
    for item in all_items:
        markup = menu_item_markup(item)
        await message.answer_photo(photo=item['url'], caption=item['name'], reply_markup=markup)


@dp.callback_query_handler(item_cb.filter(action='add'))
async def add_product_callback_handler(query: types.CallbackQuery, callback_data: dict):
    item = products.get_product(callback_data['id'])
    cart = user_cart.get_user_cart(query.message.chat.id)
    if cart is None:
        user_cart.save_user_cart({
            '_id': str(uuid.uuid4()),
            'chat_id': query.message.chat.id,
            'items': [item]
        })
    else:
        cart['items'] = [*cart['items'], item]
        user_cart.save_user_cart(cart)

    await query.answer('Товар додано до кошику')


@dp.message_handler(text=messages.contact_us)
async def cmd_contact_us(message: types.Message):
    await message.answer('Залиште Ваше повідомлення', reply_markup=None)


@dp.message_handler(text=messages.cart)
async def cmd_contact_us(message: types.Message):
    cart = user_cart.get_user_cart(message.chat.id)
    for item in cart['items']:
        markup = cart_item_markup(item)
        await message.answer_photo(photo=item['url'], caption=item['name'], reply_markup=markup)

    total_cost = reduce(lambda total, item: total + float(item['price']), cart['items'], 0)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(messages.back_to_home)
    markup.add(messages.submit_order)

    await message.answer(f'Загальна сума замовлення - {round(total_cost, 2)} грн', reply_markup=markup)


@dp.callback_query_handler(item_cb.filter(action='delete'))
async def add_product_callback_handler(query: types.CallbackQuery, callback_data: dict):
    item_id = callback_data['id']
    cart = user_cart.get_user_cart(query.message.chat.id)
    cart['items'] = [item for item in cart['items'] if item['_id'] != item_id]
    user_cart.save_user_cart(cart)

    await query.answer('Товар видалено з кошику')


async def on_startup(dp):
    products.populate_products()
    await bot.delete_webhook()
    await bot.set_webhook(configuration.WEBHOOK_URL)


async def on_shutdown():
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':

    if "HEROKU" in list(os.environ.keys()):
        executor.start_webhook(
            dispatcher=dp,
            webhook_path=configuration.WEBHOOK_PATH,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            host="",
            port="",
        )
    else:
        print("Bot has started")
        executor.start_polling(dp, on_startup=on_startup, skip_updates=False)
