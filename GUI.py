from customtkinter import *
import customtkinter
import threading
from PIL import Image, ImageTk
import DataBase
import Loc
import bot
import io

codes_list = []

# region GUI
customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

root = CTk()
height = root.winfo_screenheight() / 2
width = root.winfo_screenwidth() / 2
windowWidth = 700
windowHeight = 750
root.geometry(f"{windowWidth}x{windowHeight}+{int(width - windowWidth / 2)}+{int(height - windowHeight / 2)}")
root.title("Raffle Bot")
root.resizable(False, False)

tab_view = CTkTabview(root, height=windowHeight - 30, width=windowWidth)
codes_tab = tab_view.add("Codes")
payout_tab = tab_view.add("Payouts")

is_bot_running = BooleanVar(value=False)
denied_filter = BooleanVar(value=False)
checking_filter = BooleanVar(value=False)
confirmed_filter = BooleanVar(value=False)

run_switch = CTkCheckBox(root, text="RUN", variable=is_bot_running,
                         font=("Comic Sans MS", 15), corner_radius=90, fg_color='green', checkmark_color='green',
                         border_color='red', hover=False)

codes_frame = CTkScrollableFrame(codes_tab, border_color='gray', border_width=1)
codes_frame.pack(pady=30, fill=BOTH, expand=True)

payout_frame = CTkScrollableFrame(payout_tab, border_color='gray', border_width=1)
payout_frame.pack(pady=30, fill=BOTH, expand=True)

denied_switch = CTkCheckBox(codes_tab, text="denied", variable=denied_filter,
                            font=("Comic Sans MS", 15), corner_radius=90, fg_color='white', checkmark_color='white',
                            border_color='white', hover=False, checkbox_height=15, checkbox_width=15)
checking_switch = CTkCheckBox(codes_tab, text="checking", variable=checking_filter,
                              font=("Comic Sans MS", 15), corner_radius=90, fg_color='white', checkmark_color='white',
                              border_color='white', hover=False, checkbox_height=15, checkbox_width=15)
confirmed_switch = CTkCheckBox(codes_tab, text="confirmed", variable=confirmed_filter,
                               font=("Comic Sans MS", 15), corner_radius=90, fg_color='white', checkmark_color='white',
                               border_color='white', hover=False, checkbox_height=15, checkbox_width=15)

get_codes_btn = CTkButton(codes_tab, text="get codes", font=("Comic Sans MS", 12), width=40, height=10)

# build UI
left_padding = 15
run_switch.place(x=left_padding, y=10)
tab_view.place(x=0, y=30)
denied_switch.place(x=0, y=0)
checking_switch.place(x=100, y=0)
confirmed_switch.place(x=200, y=0)
get_codes_btn.place(x=600, y=0)


def run_bot_event():
    def run_bot():
        if not is_bot_running.get():
            print('off')
            bot.stop_bot()
        else:
            print('on')
            bot.start_bot()

    threading.Thread(target=run_bot, daemon=True).start()


def get_codes():
    res = DataBase.get_codes(denied_switch.get(), checking_switch.get(), confirmed_switch.get())
    return res


def deny_code(user_id):
    pass


def check_code(user_id):
    pass


def confirm_code(user_id):
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
    # print(item_list)
    for item in item_list:
        deny_code_btn = CTkButton(codes_frame, text="deny", font=("Comic Sans MS", 12), width=40, height=10,
                                  fg_color='red')
        checking_code_btn = CTkButton(codes_frame, text="checking", font=("Comic Sans MS", 12), width=40, height=10)
        confirm_code_btn = CTkButton(codes_frame, text="confirm", font=("Comic Sans MS", 12), width=40, height=10,
                                     fg_color='green')
        divider = CTkLabel(codes_frame, text='')
        user_id = CTkLabel(codes_frame, text=f'{item[2]}', font=("Consolas", 13))
        code = CTkLabel(codes_frame, text=item[3], font=("Consolas", 13))
        image = CTkButton(codes_frame, text="image", font=("Comic Sans MS", 12), width=40, height=10)

        user_id.grid(row=item_height, column=0, padx=0)
        code.grid(row=item_height, column=1, padx=10)
        image.grid(row=item_height, column=2, padx=10)
        divider.grid(row=item_height, column=3, padx=45)
        deny_code_btn.grid(row=item_height, column=4, padx=10)
        checking_code_btn.grid(row=item_height, column=5, padx=10)
        confirm_code_btn.grid(row=item_height, column=6, padx=10)

        image.configure(command=lambda x=item[4]: show_image(x))
        deny_code_btn.configure(command=lambda x=item[3]: deny_code(x))
        checking_code_btn.configure(command=lambda x=item[3]: check_code(x))
        confirm_code_btn.configure(command=lambda x=item[3]: confirm_code(x))

        codes_list.append(user_id)
        codes_list.append(code)
        codes_list.append(image)
        codes_list.append(deny_code_btn)
        codes_list.append(checking_code_btn)
        codes_list.append(confirm_code_btn)
        codes_list.append(divider)
        item_height += item_height_step


get_codes_btn.configure(command=refresh_codes)
run_switch.configure(command=run_bot_event)
Loc.parse_loc()
root.mainloop()
