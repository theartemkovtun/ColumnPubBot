from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

item_cb = CallbackData('item', 'id', 'action')


def menu_item_markup(item):
    global item_cb

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(f"{item['price']} грн", callback_data=item_cb.new(id=item['_id'], action='add')))

    return markup
