import telebot
from telebot.types import *
import DataBase


def save_code_screenshot(message: Message, bot: telebot.TeleBot):
    file = message.photo[-1].file_id
    f = bot.get_file(file)
    df = bot.download_file(f.file_path)
    return df


def save_code_txt(message: Message, user_id, image):
    m_code = message.text
    DataBase.set_code(user_id, m_code, image)
