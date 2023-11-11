from telebot.types import *
import DataBase
import LocKeys as Lk
from Loc import get_loc as loc
def sell_tickets(user_id, message: Message):
    sell_amount = int(message.text)
    try:
        ticket_amount = DataBase.get_user_ticket_count(user_id)
        if ticket_amount - sell_amount < 0:
            return loc(Lk.not_enough_t, user_id)
        DataBase.set_user_ticket_count(user_id, ticket_amount - sell_amount)
        DataBase.set_payout(user_id, sell_amount)
        return (f'{loc(Lk.you_sold, user_id)} {message.text} {loc(Lk.tickets, user_id)}. \n'
                f'{loc(Lk.after_confirm, user_id)}')
    except Exception as e:
        print(e)
        return loc(Lk.error, user_id)

