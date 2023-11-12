import io

from PIL import Image
from customtkinter import *

import DataBase
import bot

import LocKeys as Lk
from Loc import get_loc as loc

codes_list = []

def set_tab(codes_tab):
    codes_frame = CTkScrollableFrame(codes_tab, border_color='gray', border_width=1)
    codes_frame.pack(pady=30, fill=BOTH, expand=True)

    denied_filter = BooleanVar(value=False)
    checking_filter = BooleanVar(value=False)
    confirmed_filter = BooleanVar(value=False)

    denied_switch = CTkCheckBox(codes_tab, text="denied", variable=denied_filter,
                                font=("Comic Sans MS", 15), corner_radius=90, fg_color='white', checkmark_color='white',
                                border_color='white', hover=False, checkbox_height=15, checkbox_width=15)
    checking_switch = CTkCheckBox(codes_tab, text="checking", variable=checking_filter,
                                  font=("Comic Sans MS", 15), corner_radius=90, fg_color='white',
                                  checkmark_color='white',
                                  border_color='white', hover=False, checkbox_height=15, checkbox_width=15)
    confirmed_switch = CTkCheckBox(codes_tab, text="confirmed", variable=confirmed_filter,
                                   font=("Comic Sans MS", 15), corner_radius=90, fg_color='white',
                                   checkmark_color='white',
                                   border_color='white', hover=False, checkbox_height=15, checkbox_width=15)

    get_codes_btn = CTkButton(codes_tab, text="codes", font=("Comic Sans MS", 12), width=40, height=10)

    left_padding = 15
    denied_switch.place(x=0, y=0)
    checking_switch.place(x=100, y=0)
    confirmed_switch.place(x=200, y=0)
    get_codes_btn.place(x=600, y=0)

    def get_codes():
        res = DataBase.get_codes(denied_switch.get(), checking_switch.get(), confirmed_switch.get())
        return res

    def deny_code(user_id, btn):
        DataBase.set_code_state(user_id, 'denied')
        DataBase.add_reputation(user_id, -1)
        bot.send_notification(user_id, loc(Lk.code_denied, user_id))
        btn.configure(state='disabled')

    def check_code(user_id, btn):
        DataBase.set_code_state(user_id, 'checking')
        btn.configure(state='disabled')

    def confirm_code(user_id, btn):
        DataBase.set_code_state(user_id, 'confirmed')
        DataBase.add_reputation(user_id, 1)
        DataBase.add_tickets(user_id, 10)
        DataBase.add_code_quantity(user_id, 1)
        bot.send_notification(user_id,  loc(Lk.you_got_10t, user_id))
        try:
            DataBase.add_r_tickets(user_id)
            f_id = DataBase.get_user_f_id(user_id)
            bot.send_notification(f_id,  loc(Lk.you_got_t_from_f, user_id))
            btn.configure(state='disabled')
        except:
            pass

    def show_image(img_bytes):
        imageStream = io.BytesIO(img_bytes)
        imageFile = Image.open(imageStream)
        imageFile.show()

    def refresh_codes():
        item_height = 0
        item_height_step = 1

        for widget in codes_list:
            widget.destroy()

        item_list = get_codes()
        for item in item_list:
            deny_code_btn = CTkButton(codes_frame, text="deny", font=("Comic Sans MS", 12), width=40, height=10,
                                      fg_color='red')
            checking_code_btn = CTkButton(codes_frame, text="checking", font=("Comic Sans MS", 12), width=40, height=10)
            confirm_code_btn = CTkButton(codes_frame, text="confirm", font=("Comic Sans MS", 12), width=40, height=10,
                                         fg_color='green')
            divider = CTkLabel(codes_frame, text='')
            user_id = CTkLabel(codes_frame, text=f'{item[1]}', font=("Consolas", 13))
            code = CTkLabel(codes_frame, text=item[2], font=("Consolas", 13))
            image = CTkButton(codes_frame, text="image", font=("Comic Sans MS", 12), width=40, height=10)

            user_id.grid(row=item_height, column=0, padx=0)
            code.grid(row=item_height, column=1, padx=10)
            image.grid(row=item_height, column=2, padx=10)
            divider.grid(row=item_height, column=3, padx=45)
            deny_code_btn.grid(row=item_height, column=4, padx=10)
            checking_code_btn.grid(row=item_height, column=5, padx=10)
            confirm_code_btn.grid(row=item_height, column=6, padx=10)

            if item[4] == 'denied' or item[4] == 'confirmed':
                deny_code_btn.configure(state='disabled')
                confirm_code_btn.configure(state='disabled')
                checking_code_btn.configure(state='disabled')

            image.configure(command=lambda x=item[3]: show_image(x))
            deny_code_btn.configure(command=lambda x=item[1], btn=deny_code_btn: deny_code(x, btn))
            checking_code_btn.configure(command=lambda x=item[1], btn=checking_code_btn: check_code(x, btn))
            confirm_code_btn.configure(command=lambda x=item[1], btn=confirm_code_btn: confirm_code(x, btn))

            codes_list.append(user_id)
            codes_list.append(code)
            codes_list.append(image)
            codes_list.append(deny_code_btn)
            codes_list.append(checking_code_btn)
            codes_list.append(confirm_code_btn)
            codes_list.append(divider)
            item_height += item_height_step

    get_codes_btn.configure(command=refresh_codes)
