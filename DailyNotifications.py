import time
import schedule
import DataBase
import bot

import LocKeys as Lk
from Loc import get_loc as loc

def notify(n_type):
    users = DataBase.get_users()

    for user_id in users:
        if n_type == 1:
            text = loc(Lk.notifi_1, user_id)
        else:
            text = loc(Lk.notifi_2, user_id)

        bot.send_notification(user_id[0], text)

def subscribe_notifications():
    schedule.every().day.at('8:0:0').do(lambda: notify(1))
    schedule.every().day.at('20:0:0').do(lambda: notify(2))

def run_notifications():
    while True:
        schedule.run_pending()
        time.sleep(1)
