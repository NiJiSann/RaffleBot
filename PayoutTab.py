from customtkinter import *

import DataBase
import bot

import LocKeys as Lk
from Loc import get_loc as loc

payout_list = []


def set_tab(tab):
    payout_frame = CTkScrollableFrame(tab, border_color='gray', border_width=1)
    payout_frame.pack(pady=30, fill=BOTH, expand=True)

    unpaid_filter = BooleanVar(value=False)

    unpaid_switch = CTkCheckBox(tab, text="unpaid", variable=unpaid_filter,
                                font=("Comic Sans MS", 15), corner_radius=90, fg_color='white', checkmark_color='white',
                                border_color='white', hover=False, checkbox_height=15, checkbox_width=15)

    get_payouts_btn = CTkButton(tab, text="payouts", font=("Comic Sans MS", 12), width=40, height=10)

    unpaid_switch.place(x=0, y=0)
    get_payouts_btn.place(x=600, y=0)

    def get_payouts():
        res = DataBase.get_payouts(unpaid_filter.get())
        return res

    def payed(user_id, btn):
        btn.configure(state='disabled')
        DataBase.set_payout_state(user_id, 'paid')
        bot.send_notification(user_id, loc(Lk.tickets_sold, user_id))
        pass

    def refresh_payouts():
        item_height = 0
        item_height_step = 1

        for widget in payout_list:
            widget.destroy()

        item_list = get_payouts()
        for item in item_list:
            pay_btn = CTkButton(payout_frame, text="payed", font=("Comic Sans MS", 12), width=40, height=10,
                                fg_color='red')

            divider = CTkLabel(payout_frame, text='')
            user_id = CTkLabel(payout_frame, text=f'{item[0]}', font=("Consolas", 13))
            tickets = CTkLabel(payout_frame, text=item[1], font=("Consolas", 13), text_color='red')
            wallet = CTkLabel(payout_frame, text=item[2], font=("Consolas", 13), text_color='green')
            status = CTkLabel(payout_frame, text=item[3], font=("Consolas", 13))

            user_id.grid(row=item_height, column=0, padx=0)
            tickets.grid(row=item_height, column=1, padx=10)
            wallet.grid(row=item_height, column=2, padx=10)
            divider.grid(row=item_height, column=3, padx=50)
            status.grid(row=item_height, column=4, padx=10)
            pay_btn.grid(row=item_height, column=5, padx=10)

            if item[3] == 'paid':
                pay_btn.configure(state='disabled')

            pay_btn.configure(command=lambda x=item[0], btn=pay_btn: payed(x, btn))

            payout_list.append(user_id)
            payout_list.append(tickets)
            payout_list.append(wallet)
            payout_list.append(divider)
            payout_list.append(status)
            payout_list.append(pay_btn)
            item_height += item_height_step

    get_payouts_btn.configure(command=refresh_payouts)
