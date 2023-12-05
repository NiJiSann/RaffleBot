import uuid
from telebot.types import *
import DataBase
import LocKeys as Lk
from Loc import get_loc as loc


def set_user_info(message: Message):
    user_id = message.from_user.id
    user_first_name = message.from_user.first_name
    user_last_name = message.from_user.last_name
    username = message.from_user.username
    user_data = DataBase.get_user(user_id)
    if not user_data:
        DataBase.set_user(user_first_name, user_id, str(uuid.uuid4()), user_last_name, username)


def get_profile_info(user_id):
    user_data = DataBase.get_user(user_id)
    return (f'{loc(Lk.name, user_id)}: {user_data[0][0]} \n'
            f'{loc(Lk.tickets, user_id)}: {user_data[0][7]}\n'
            f'{loc(Lk.reputation, user_id)}: {user_data[0][3]}\n')


def get_referral_code(user_id):
    return DataBase.get_user_r_code(user_id)


def set_wallet(message: Message, user_id):
    DataBase.set_wallet(user_id, message.text)
    return loc(Lk.success, user_id)


def set_friend_referral(message: Message, user_id):
    DataBase.set_friend_referral(user_id, message.text)
    return loc(Lk.success, user_id)
