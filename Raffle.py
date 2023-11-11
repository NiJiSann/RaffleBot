from telebot.types import *
import DataBase
import LocKeys as Lk
from Loc import get_loc as loc


def show_raffle_100(user_id):
    raffle_cost = 10
    kb = InlineKeyboardMarkup()
    btn = InlineKeyboardButton(text=f"{loc(Lk.participate, user_id)}: {raffle_cost} {loc(Lk.tickets, user_id)}",
                               callback_data='raffle100')
    kb.add(btn)
    total_participants = 100
    current_participants = len(DataBase.get_raffle100())
    text = (loc(Lk.raffle_100, user_id) +
            f'\n\n{loc(Lk.participants, user_id)}: {current_participants}/{total_participants}')

    return kb, text


def buy_raffle100(user_id):
    raffle_price = 10
    try:
        ticket_amount = DataBase.get_user_ticket_count(user_id)
        if ticket_amount - raffle_price < 0:
            return loc(Lk.not_enough_t, user_id)
        DataBase.set_user_ticket_count(user_id, ticket_amount - raffle_price)
        DataBase.set_raffle_p(user_id)
        return loc(Lk.you_bought_seat, user_id)
    except:
        return loc(Lk.error, user_id)

