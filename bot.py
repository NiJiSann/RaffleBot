import telebot
from telebot.types import *

import DataBase
import Extentions
import GetCode
import HandlerFunc
import Layout
import Loc
import Raffle
import Sell
import UserInfo
import LocKeys as Lk
from Loc import get_loc as loc

bot = telebot.TeleBot("6892712987:AAFoxkiA7cxc9dIJxOE9wyXSVV2jJ1mO8xc")

code_pattern = r'^[A-Z0-9]{4}-[A-Z0-9]{4}-[A-Z0-9]{5}-[A-Z0-9]{4}-[A-Z0-9]{4}$'
wallet_pattern = r"[a-zA-Z0-9]{32}"
referral_code_pattern = r"[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}"
num_patter = r'^[0-9]+$'
code_state = False
wallet_state = False
referral_state = False
sell_state = False
image_byte = b'0'

main_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
code_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
raffle_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
sell_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
profile_btn = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)

# region  command section
@bot.message_handler(commands=['help'])
def h(message: Message):
    user_id = message.from_user.id
    bot.send_message(user_id, f"{loc(Lk.hlp, user_id)}")

@bot.message_handler(commands=['start'])
def start(message: Message):
    user_id = message.from_user.id
    res = UserInfo.set_user_info(message)
    bot.send_message(user_id, res)
    show_languages(user_id)

# endregion

# region choose loc
def show_languages(user_id):
    res = Loc.show_loc()
    bot.send_message(user_id, res[1], reply_markup=res[0])

@bot.callback_query_handler(func=lambda callback: callback.data)
def set_loc(callback: CallbackQuery):
    user_id = callback.from_user.id
    DataBase.set_user_loc(user_id, callback.data)
    global main_btn
    main_btn = Extentions.add_buttons(main_btn, Layout.get_main_layout(user_id))
    bot.send_message(user_id, f"{loc(Lk.thanks, user_id)}", reply_markup=main_btn)

# endregion

# region my profile section
@bot.message_handler(func=HandlerFunc.my_profile)
def my_profile(message: Message):
    user_id = message.from_user.id
    res = UserInfo.get_profile_info(user_id)
    global profile_btn
    profile_btn = Extentions.add_buttons(profile_btn, Layout.get_profile_layout(user_id))
    bot.send_message(user_id, res, reply_markup=profile_btn)


@bot.message_handler(func=HandlerFunc.my_referral)
def referral(message: Message):
    user_id = message.from_user.id
    res = UserInfo.get_referral_code(user_id)
    bot.send_message(user_id, res)


@bot.message_handler(func=HandlerFunc.set_wallet)
def wallet(message: Message):
    global wallet_state, referral_state
    referral_state = False
    wallet_state = True
    user_id = message.from_user.id
    bot.send_message(user_id, loc(Lk.send_wallet_address, user_id))


@bot.message_handler(regexp=wallet_pattern)
def set_wallet(message: Message):
    global wallet_state
    wallet_state = False
    user_id = message.from_user.id
    res = UserInfo.set_wallet(message, user_id)
    bot.send_message(user_id, res)


@bot.message_handler(func=HandlerFunc.set_f_referral)
def friend_referral(message: Message):
    global referral_state, wallet_state
    wallet_state = False
    referral_state = True
    user_id = message.from_user.id
    bot.send_message(user_id, loc(Lk.send_r_code, user_id))


@bot.message_handler(regexp=referral_code_pattern)
def set_wallet(message: Message):
    global referral_state
    referral_state = False
    user_id = message.from_user.id
    res = UserInfo.set_friend_referral(message, user_id)
    bot.send_message(user_id, res)
# endregion

# region code section
@bot.message_handler(func=HandlerFunc.send_code)
def choose_code(message: Message):
    user_id = message.from_user.id
    global code_btn
    code_btn = Extentions.add_buttons(code_btn, Layout.get_code_layout(user_id))
    bot.send_message(user_id, loc(Lk.code_type, user_id), reply_markup=code_btn)

@bot.message_handler(regexp=r'(Overwatch|Roblox)')
def send_code_img(message: Message):
    user_id = message.from_user.id
    bot.send_message(user_id, loc(Lk.screenshot, user_id))

@bot.message_handler(content_types=['photo'])
def receive_code(message: Message):
    global code_state, image_byte
    code_state = True
    user_id = message.from_user.id
    image_byte = GetCode.save_code_screenshot(message, bot)
    bot.send_message(user_id, loc(Lk.send_code_txt, user_id))

@bot.message_handler(regexp=code_pattern)
def receive_code_txt(message: Message):
    global code_state
    code_state = False
    user_id = message.from_user.id
    GetCode.save_code_txt(message, user_id, image_byte)
    global main_btn
    main_btn = Extentions.add_buttons(main_btn, Layout.get_main_layout(user_id))
    bot.send_message(user_id, loc(Lk.thx_wait, user_id), reply_markup=main_btn)
# endregion

# region raffle section
@bot.message_handler(func=HandlerFunc.raffle)
def raffle(message: Message):
    user_id = message.from_user.id
    global raffle_btn
    raffle_btn = Extentions.add_buttons(raffle_btn, Layout.get_raffle_layout(user_id))
    bot.send_message(user_id, loc(Lk.choose_raffle, user_id), reply_markup=raffle_btn)


@bot.message_handler(func=HandlerFunc.raffle100)
def raffle100(message: Message):
    user_id = message.from_user.id
    res = Raffle.show_raffle_100(user_id)
    bot.send_message(user_id, res[1], reply_markup=res[0])

@bot.callback_query_handler(func=lambda callback: callback.data)
def buy_raffle100_seat(callback: CallbackQuery):
    if not callback.data == 'raffle100':
        return

    user_id = callback.from_user.id
    res = Raffle.buy_raffle100(user_id)
    bot.send_message(user_id, res)

# endregion

# region sell section
@bot.message_handler(func=HandlerFunc.sell_tickets)
def sell(message: Message):
    global sell_state
    sell_state = True
    user_id = message.from_user.id
    res = (f'{loc(Lk.you_have, user_id)}: {DataBase.get_user_ticket_count(user_id)} {loc(Lk.tickets, user_id)} \n'
           f'{loc(Lk.sell_tickets_amount, user_id)}')
    global sell_btn
    sell_btn = Extentions.add_buttons(sell_btn, Layout.get_sell_layout(user_id))
    bot.send_message(user_id, res, reply_markup=sell_btn)

@bot.message_handler(regexp=num_patter)
def sell(message: Message):
    global sell_state
    if not sell_state:
        delete_last_message(message)
        return
    sell_state = False
    user_id = message.from_user.id
    res = Sell.sell_tickets(user_id, message)
    global main_btn
    main_btn = Extentions.add_buttons(main_btn, Layout.get_main_layout(user_id))
    bot.send_message(user_id, res, reply_markup=main_btn)
# endregion

# region common section
@bot.message_handler(func=HandlerFunc.back)
def back(message: Message):
    user_id = message.from_user.id
    global main_btn
    main_btn = Extentions.add_buttons(main_btn, Layout.get_main_layout(user_id))
    bot.send_message(user_id, "'_'", reply_markup=main_btn)


@bot.message_handler()
def delete_last_message(message: Message):
    global sell_state, profile_btn, code_btn, main_btn
    user_id = message.from_user.id

    if code_state:
        code_btn = Extentions.add_buttons(code_btn, Layout.get_code_layout(user_id))
        bot.reply_to(message, loc(Lk.invalid_code, user_id), reply_markup=code_btn)
        return
    if wallet_state:
        profile_btn = Extentions.add_buttons(profile_btn, Layout.get_profile_layout(user_id))
        bot.reply_to(message, loc(Lk.invalid_address, user_id), reply_markup=profile_btn)
        return
    if referral_state:
        profile_btn = Extentions.add_buttons(profile_btn, Layout.get_profile_layout(user_id))
        bot.reply_to(message, loc(Lk.invalid_referral, user_id), reply_markup=profile_btn)
        return
    if sell_state:
        sell_state = False
        main_btn = Extentions.add_buttons(main_btn, Layout.get_main_layout(user_id))
        bot.reply_to(message, loc(Lk.invalid_input, user_id), reply_markup=main_btn)
        return
    bot.delete_message(chat_id=user_id, message_id=message.message_id)
# endregion

def start_bot():
    bot.polling()

def stop_bot():
    bot.stop_bot()

# J658-HP4N-QNMLS-FRHN-FHLB
