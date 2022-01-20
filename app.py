

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
import configuration
import os
from domain import products, users, user_cart, user_feedback
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup
import messages
from keyboards.menu_item import item_cb, menu_item_markup
from keyboards.all_items import all_items_markup
from keyboards.cart_item import cart_cb, cart_item_markup
from functools import reduce
import uuid

bot = Bot(token=configuration.TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
new_item = {}


@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    if users.check_if_user_admin(message.chat.id):
        markup = ReplyKeyboardMarkup(selective=True, one_time_keyboard=True)
        markup.add(messages.add_item)
        markup.add(messages.all_products)

        await message.answer(f'{message.chat.first_name}, '
                f'Ласкаво просимо до ColumnPub чат боту. Ваша роль адмін', reply_markup=markup)
    else:
        users.add_user({
            "_id": str(uuid.uuid4()),
            "role": "2",
            "chat_id": message.chat.id,
            "fullname": message.chat.full_name,
            '_address': ''
        })

        markup = ReplyKeyboardMarkup(selective=True)
        markup.add(messages.menu)
        markup.add(messages.contact_us)
        markup.add(messages.cart)

        await message.answer(f'{message.chat.first_name}, '
                f'Ласкаво просимо до ColumnPub чат боту. Дякуємо, що обрали наш ресторан', reply_markup=markup)


class Add_New_Items(StatesGroup):
    addName = State()
    addPhoto = State()
    addPrice = State()
    confirm = State()


@dp.message_handler(text=messages.add_item)
async def cmd_add_item(message: types.Message):
    if users.check_if_user_admin(message.chat.id):
        await Add_New_Items.addName.set()
        await message.answer('Введіть назву товару:', reply_markup=None)


@dp.message_handler(state=Add_New_Items.addName)
async def cmd_addName(message: types.Message):
    if users.check_if_user_admin(message.chat.id):
        new_item['name'] = message.text
        await Add_New_Items.addPhoto.set()
        await message.answer('Додайте посилання на фото товару', reply_markup=None)


@dp.message_handler(state=Add_New_Items.addPhoto)
async def cmd_add_photo(message: types.Message):
    if users.check_if_user_admin(message.chat.id):
        new_item['url'] = message.text
        await Add_New_Items.addPrice.set()
        await message.answer('Додайте ціну товару', reply_markup=None)


@dp.message_handler(state=Add_New_Items.addPrice)
async def cmd_add_price(message: types.Message):
    if users.check_if_user_admin(message.chat.id):
        if not message.text.isnumeric():
            await Add_New_Items.addPrice.set()
            await message.answer('Додайте іншу ціну товару', reply_markup=None)
            return
        new_item['price'] = int(message.text)
        new_item['_id'] = str(uuid.uuid4())
        markup = menu_item_markup(new_item)
        await message.answer_photo(photo=new_item['url'], caption=new_item['name'], reply_markup=markup)
        markup = ReplyKeyboardMarkup(selective=True, one_time_keyboard=True)
        markup.add(messages.yes)
        markup.add(messages.no)
        await Add_New_Items.confirm.set()
        await message.answer('Підтвердіть додавання нового товару', reply_markup=markup)


@dp.message_handler(state=Add_New_Items.confirm)
async def cmd_confirm(message: types.Message, state: FSMContext):
    if users.check_if_user_admin(message.chat.id):
        if message.text == messages.yes:
            products.add_product(new_item)

            markup = ReplyKeyboardMarkup(selective=True, one_time_keyboard=True)
            markup.add(messages.add_item)
            markup.add(messages.all_products)

            await message.answer('Товар успішно додано', reply_markup=markup)
        elif message.text == messages.no:
            markup = ReplyKeyboardMarkup(selective=True, one_time_keyboard=True)
            markup.add(messages.add_item)
            markup.add(messages.all_products)

            dict.clear(new_item)
            await message.answer('Товар видалено', reply_markup=markup)
        await state.finish()


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


@dp.message_handler(text=messages.all_products)
async def cmd_menu(message: types.Message):
    all_items = products.get_products()
    for item in all_items:
        markup = all_items_markup(item)
        await message.answer_photo(photo=item['url'], caption=f'{item["name"]} - {item["price"]} грн', reply_markup=markup)


@dp.callback_query_handler(item_cb.filter(action='delete_product'))
async def add_product_callback_handler(query: types.CallbackQuery, callback_data):
    item_id = callback_data['id']
    products.delete_product(item_id)

    await query.answer('Товар видалено')



@dp.callback_query_handler(item_cb.filter(action='add'))
async def add_product_callback_handler(query: types.CallbackQuery, callback_data: dict):
    item = products.get_product(callback_data['id'])
    item['_id'] = str(uuid.uuid4())
    cart = user_cart.get_user_cart(query.message.chat.id)
    if cart is None:
        user_cart.save_user_cart({
            '_id': str(uuid.uuid4()),
            'chat_id': query.message.chat.id,
            'items': [item],
        })
    else:
        cart['items'] = [*cart['items'], item]
        user_cart.save_user_cart(cart)

    await query.answer('Товар додано до кошику')


class FSMAState(StatesGroup):
    address = State()


class FSMAState2(StatesGroup):
    add_feedback = State()


@dp.message_handler(text=messages.contact_us)
async def cmd_contact_us(message: types.Message):
    await FSMAState2.add_feedback.set()
    await message.answer('Залиште Ваше повідомлення', reply_markup=None)


@dp.message_handler(state=FSMAState2.add_feedback)
async def cmd_add_address(message: types.Message, state: FSMContext):
    user = users.get_user(message.chat.id)

    user_feedback.add_feedback({
        '_id': str(uuid.uuid4()),
        'username': user['fullname'],
        'chat_id': message.chat.id,
        'feedback_text': message.text
    })
    await state.finish()

    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(messages.back_to_home)
    await message.answer(f'Відгук - "{message.text}" успішно доданий', reply_markup=markup)


@dp.message_handler(text=messages.submit_order)
async def cmd_submit_order(message: types.Message):
    user = users.get_user(message.chat.id)
    if users.check_user_has_address(user['_id']):
        await FSMAState.address.set()
        await message.reply('Адреса відсутня! \nВведіть адресу:', reply_markup=None)
    else:
        markup = ReplyKeyboardMarkup(selective=True, one_time_keyboard=True)
        markup.add(messages.yes)
        markup.add(messages.no)

        await message.reply(f'Ваша адреса: {user["_address"]}?', reply_markup=markup)


@dp.message_handler(text=messages.yes)
async def cmd_confirm_address(message: types.Message):
    user = users.get_user(message.chat.id)
    answer = 'Ваше замовлення: '
    items = user_cart.get_user_cart(message.chat.id)['items']
    cur_prods = products.get_products()
    i = 1
    for prod in cur_prods:
        prod_sum = sum(1 for item in items if item['name'] == prod['name'])
        if prod_sum > 0:
            answer = answer + '\n1) ' + str(prod['name']) + ' x' + str(prod_sum) + ';  '
        i += 1
    total_cost = reduce(lambda total, item: total + float(item['price']), items, 0)
    answer = answer + f'\nЗагальна сума замовлення - {round(total_cost, 2)} грн \n'
    answer = answer + f'Кур’єр доставить вам замовлення на {user["_address"]} \n'
    answer = answer + f'Кур’єр зв’яжеться з вами. Смачного!'
    await message.answer(answer, reply_markup=None)

    user_cart.delete_user_cart(message.chat.id)
    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(messages.menu)
    markup.add(messages.contact_us)
    markup.add(messages.cart)

    await message.answer('Головна сторінка', reply_markup=markup)


@dp.message_handler(text=messages.no)
async def cmd_not_confirm_address(message: types.Message):
    user = users.get_user(message.chat.id)
    await FSMAState.address.set()
    await message.reply('Адресу видалено! \nВведіть нову адресу:', reply_markup=None)


@dp.message_handler(text=messages.cart)
async def cmd_contact_us(message: types.Message):
    cart = user_cart.get_user_cart(message.chat.id)

    if cart is None or not cart['items']:
        await message.answer('Кошик пустий')
        return

    for item in cart['items']:
        markup = cart_item_markup(item)
        await message.answer_photo(photo=item['url'], caption=item['name'], reply_markup=markup)

    total_cost = reduce(lambda total, item: total + float(item['price']), cart['items'], 0)

    markup = ReplyKeyboardMarkup(resize_keyboard=True, selective=True)
    markup.add(messages.back_to_home)
    markup.add(messages.submit_order)

    await message.answer(f'Загальна сума замовлення - {round(total_cost, 2)} грн', reply_markup=markup)


@dp.message_handler(state=FSMAState.address)
async def cmd_add_address(message: types.Message, state: FSMContext):
    user = users.get_user(message.chat.id)
    user['_address'] = message.text
    users.add_user(user)
    await state.finish()

    markup = ReplyKeyboardMarkup(selective=True)
    markup.add(messages.back_to_home)
    markup.add(messages.submit_order)
    await message.answer(f'Адреса - {message.text} успішно додана', reply_markup=markup)


@dp.callback_query_handler(item_cb.filter(action='delete'))
async def add_product_callback_handler(query: types.CallbackQuery, callback_data: dict):
    item_id = callback_data['id']
    cart = user_cart.get_user_cart(query.message.chat.id)
    cart['items'] = [item for item in cart['items'] if item['_id'] != item_id]
    user_cart.save_user_cart(cart)

    await query.answer('Товар видалено з кошику')


async def on_startup(dp):
    products.populate_products()
    users.add_admin()
    await bot.delete_webhook()
    await bot.set_webhook(configuration.WEBHOOK_URL)


async def on_shutdown():
    await bot.delete_webhook()
    await dp.storage.close()
    await dp.storage.wait_closed()


if __name__ == '__main__':
    print("Bot has started")
    executor.start_polling(dp, on_startup=on_startup, skip_updates=False)


