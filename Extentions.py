from telebot.types import *


def add_buttons(keyboard: ReplyKeyboardMarkup, list_of_btn):
    buttons = []
    kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=keyboard.row_width)
    for btn in list_of_btn:
        buttons.append(KeyboardButton(btn))
    kb.add(*buttons)
    return kb
