import threading
import time
import schedule
import DataBase
import bot

import LocKeys as Lk
from Loc import get_loc as loc


def notify(n_type):
    users = DataBase.get_users('user_id')

    for user_id in users:
        if n_type == 1:
            text = loc(Lk.notify_1, user_id)
        else:
            text = loc(Lk.notify_2, user_id)

        bot.send_notification(user_id[0], text)


def subscribe_notifications():
    schedule.every().day.at('08:00:00').do(lambda: notify(1))
    schedule.every().day.at('20:00:00').do(lambda: notify(2))


def run_notifications():
    def run():
        while True:
            schedule.run_pending()
            time.sleep(1)

    threading.Thread(target=run, daemon=True).start()
