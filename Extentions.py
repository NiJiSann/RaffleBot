from telebot.types import *

def add_buttons(keyboard: ReplyKeyboardMarkup, list_of_btn):
    buttons = []
    for btn in list_of_btn:
        buttons.append(KeyboardButton(btn))
    keyboard.add(*buttons)
    return keyboard
