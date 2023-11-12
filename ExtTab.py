from customtkinter import *

import DataBase
import bot

payout_list = []

def set_tab(tab):
    # Stats
    stats_label = CTkLabel(tab, text='Statistics:\n', font=("Comic Sans MS", 20))
    users_label = CTkLabel(tab, text='Users count:\n', font=("Comic Sans MS", 15))
    codes_label = CTkLabel(tab, text='Codes count:\n', font=("Comic Sans MS", 15))
    tickets_label = CTkLabel(tab, text='Tickets count:\n', font=("Comic Sans MS", 15))
    refresh_stats_btn = CTkButton(tab, text="refresh", font=("Comic Sans MS", 12), width=40, height=10)

    # Send Message To user
    send_m_label = CTkLabel(tab, text='Send Message:\n', font=("Comic Sans MS", 20))
    user_id_label = CTkLabel(tab, text='User ID:\n', font=("Comic Sans MS", 15))
    user_loc_label = CTkLabel(tab, text='User Loc:\n', font=("Comic Sans MS", 15))
    user_id_entry = CTkEntry(tab, width=100, height=10)
    set_id_btn = CTkButton(tab, text="set id", font=("Comic Sans MS", 12), width=40, height=10)
    message_box = CTkTextbox(tab, width=500, height=100)
    send_message_btn = CTkButton(tab, text="send", font=("Comic Sans MS", 12), width=40, height=10)

    # User  Info
    user_info_label = CTkLabel(tab, text='User Info:\n', font=("Comic Sans MS", 20))
    user_id_label1 = CTkLabel(tab, text='User ID:\n', font=("Comic Sans MS", 15))
    user_id_entry1 = CTkEntry(tab, width=100, height=10)
    user_name_label = CTkLabel(tab, text='Name:\n', font=("Comic Sans MS", 15))
    username_label = CTkLabel(tab, text='Username:\n', font=("Comic Sans MS", 15))
    user_reputation_label = CTkLabel(tab, text='Reputation:\n', font=("Comic Sans MS", 15))
    user_tickets_label = CTkLabel(tab, text='Tickets count:\n', font=("Comic Sans MS", 15))
    user_codes_label = CTkLabel(tab, text='Codes count:\n', font=("Comic Sans MS", 15))
    wallet_label = CTkLabel(tab, text='Wallet:\n', font=("Comic Sans MS", 15))
    get_info_btn = CTkButton(tab, text="get", font=("Comic Sans MS", 12), width=40, height=10)

    # region build UI
    left_padding = 10
    stats_label.place(x=left_padding, y=0)
    refresh_stats_btn.place(x=left_padding + 100, y=5)
    users_label.place(x=left_padding, y=30)
    codes_label.place(x=left_padding, y=50)
    tickets_label.place(x=left_padding, y=70)

    send_m_label.place(x=left_padding, y=100)
    user_id_label.place(x=left_padding, y=130)
    user_id_entry.place(x=left_padding + 70, y=130)
    user_loc_label.place(x=left_padding + 180, y=130)
    set_id_btn.place(x=left_padding + 300, y=130)
    message_box.place(x=left_padding, y=170)
    send_message_btn.place(x=left_padding, y=280)

    user_info_label.place(x=left_padding, y=320)
    user_id_label1.place(x=left_padding, y=360)
    user_id_entry1.place(x=left_padding + 70, y=360)
    get_info_btn.place(x=left_padding + 200, y=360)
    user_name_label.place(x=left_padding, y=380)
    username_label.place(x=left_padding, y=400)
    user_reputation_label.place(x=left_padding, y=420)
    user_tickets_label.place(x=left_padding, y=440)
    user_codes_label.place(x=left_padding, y=460)
    wallet_label.place(x=left_padding, y=480)

    # endregion
    def refresh_stats():
        data = DataBase.get_users('*')
        users_count_text = f'Users count: {len(data)}\n'
        codes_count = 0
        tickets_count = 0
        users_label.configure(text=users_count_text)

        for user in data:
            print(data)
            codes_count += user[8]
            tickets_count += user[7]

        codes_count_text = f'Codes count: {codes_count}\n'
        tickets_count_text = f'Tickets count: {tickets_count}\n'

        codes_label.configure(text=codes_count_text)
        tickets_label.configure(text=tickets_count_text)

    def set_user_id():
        loc = DataBase.get_user_loc(int(user_id_entry.get()))
        loc_text = f'User Loc: {loc}\n'
        user_loc_label.configure(text=loc_text)

    def send_message():
        bot.send_notification(user_id_entry.get(), message_box.get(0))

    def get_user_info():
        data = DataBase.get_user(int(user_id_entry1.get()))[0]
        user_name_text = f'Name: {data[0]} {data[1]}\n'
        username_text = f'Username: {data[2]}\n'
        user_reputation_text = f'Reputation: {data[3]}\n'
        user_tickets_text = f'Tickets count: {data[7]}\n'
        user_codes_text = f'Codes count: {data[8]}\n'
        wallet_text = f'Wallet: {data[9]}\n'

        user_name_label.configure(text=user_name_text)
        username_label.configure(text=username_text)
        user_reputation_label.configure(text=user_reputation_text)
        user_tickets_label.configure(text=user_tickets_text)
        user_codes_label.configure(text=user_codes_text)
        wallet_label.configure(text=wallet_text)

    get_info_btn.configure(command=get_user_info)
    send_message_btn.configure(command=send_message)
    set_id_btn.configure(command=set_user_id)
    refresh_stats_btn.configure(command=refresh_stats)
