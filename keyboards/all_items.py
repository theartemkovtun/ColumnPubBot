from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

all_item_cb = CallbackData('item', 'id', 'action')


def all_items_markup(item):
    global all_item_cb

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(f"Видалити", callback_data=all_item_cb.new(id=item['_id'], action='delete_product')))

    return markup
