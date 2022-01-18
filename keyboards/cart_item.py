from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

cart_cb = CallbackData('item', 'id', 'action')


def cart_item_markup(item):
    global cart_cb

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(f"Видалити", callback_data=cart_cb.new(id=item['_id'], action='delete')))

    return markup
