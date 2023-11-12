from customtkinter import *
import customtkinter
import threading

import CodesTab
import DailyNotifications
import ExtTab
import Loc
import PayoutTab
import RaffleTab
import bot

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
raffle_tab = tab_view.add("Raffle 100")
ext_tab = tab_view.add("  ext  ")

CodesTab.set_tab(codes_tab)
RaffleTab.set_tab(raffle_tab)
PayoutTab.set_tab(payout_tab)
ExtTab.set_tab(ext_tab)

is_bot_running = BooleanVar(value=False)

run_switch = CTkCheckBox(root, text="RUN", variable=is_bot_running,
                         font=("Comic Sans MS", 15), corner_radius=90, fg_color='green', checkmark_color='green',
                         border_color='red', hover=False)

# build UI
left_padding = 15
run_switch.place(x=left_padding, y=10)
tab_view.place(x=0, y=30)

def run_bot_event():
    def run_bot():
        if not is_bot_running.get():
            bot.stop_bot()
        else:
            bot.start_bot()

    threading.Thread(target=run_bot, daemon=True).start()


run_switch.configure(command=run_bot_event)
DailyNotifications.subscribe_notifications()
DailyNotifications.run_notifications()
Loc.parse_loc()
root.mainloop()
