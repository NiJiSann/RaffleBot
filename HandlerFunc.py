from telebot.types import Message
from Loc import get_loc as loc
import LocKeys as Lk

def my_profile(message: Message):
    return message.text == loc(Lk.my_profile, message.from_user.id)

def my_referral(message: Message):
    return message.text == loc(Lk.referral_code, message.from_user.id)

def set_wallet(message: Message):
    return message.text == loc(Lk.set_wallet, message.from_user.id)

def set_f_referral(message: Message):
    return message.text == loc(Lk.set_r_code, message.from_user.id)

def send_code(message: Message):
    return message.text == loc(Lk.send_code, message.from_user.id)

def raffle(message: Message):
    return message.text == loc(Lk.raffle, message.from_user.id)

def raffle100(message: Message):
    return f'{loc(Lk.raffle, message.from_user.id)} 100' in message.text

def sell_tickets(message: Message):
    return message.text == loc(Lk.sell_tickets, message.from_user.id)

def back(message: Message):
    return message.text == loc(Lk.back, message.from_user.id)

