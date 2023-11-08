import sys
import telebot
from telebot.types import *
import DataBase

def save_code_screenshot(message: Message, bot: telebot.TeleBot):
    file = message.photo[-1].file_id
    f = bot.get_file(file)
    image_bin = bin(int.from_bytes(bot.download_file(f.file_path), byteorder=sys.byteorder))
    return image_bin

def save_code_txt(message: Message, user_id, image_bin):
    m_code = message.text
    DataBase.add_code(user_id, m_code, image_bin)

