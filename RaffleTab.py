import random
from customtkinter import *
import DataBase

raffle_list = []

def set_tab(tab):
    raffle_frame = CTkScrollableFrame(tab, border_color='gray', border_width=1)
    raffle_frame.pack(pady=30, fill=BOTH, expand=True)

    get_raffle_btn = CTkButton(tab, text="raffle", font=("Comic Sans MS ", 12), width=40, height=10)
    get_random_btn = CTkButton(tab, text="get random user", font=("Comic Sans MS ", 12), width=40, height=10)

    get_random_btn.place(x=500, y=0)
    get_raffle_btn.place(x=625, y=0)

    def get_random():
        try:
            raffle100_data = get_raffle()
            length = len(raffle100_data)
            random_num = random.randint(0, length-1)
            rand_user = raffle100_data[random_num]
        except:
            return

        for widget in raffle_list:
            widget.destroy()

        num = CTkLabel(raffle_frame, text='1', font=("Consolas", 13))
        user_id = CTkLabel(raffle_frame, text=rand_user[0], font=("Consolas", 13))
        wallet = CTkLabel(raffle_frame, text=rand_user[1], font=("Consolas", 13), text_color='green')

        num.grid(row=0, column=1, padx=10)
        user_id.grid(row=0, column=0, padx=0)
        wallet.grid(row=0, column=2, padx=10)

        raffle_list.append(num)
        raffle_list.append(user_id)
        raffle_list.append(wallet)

    def get_raffle():
        return DataBase.get_raffle100()

    def refresh_raffle():
        item_height = 0
        item_height_step = 1

        for widget in raffle_list:
            widget.destroy()

        item_list = get_raffle()
        for item in item_list:
            num = CTkLabel(raffle_frame, text=str(item_height+1), font=("Consolas", 13))
            user_id = CTkLabel(raffle_frame, text=item[0], font=("Consolas", 13), text_color='red')
            wallet = CTkLabel(raffle_frame, text=item[1], font=("Consolas", 13))

            num.grid(row=item_height, column=1, padx=10)
            user_id.grid(row=item_height, column=0, padx=0)
            wallet.grid(row=item_height, column=2, padx=10)

            raffle_list.append(num)
            raffle_list.append(user_id)
            raffle_list.append(wallet)
            item_height += item_height_step

    get_random_btn.configure(command=get_random)
    get_raffle_btn.configure(command=refresh_raffle)