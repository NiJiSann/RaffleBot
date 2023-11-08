import LocKeys as Lk
from Loc import get_loc as loc

def get_main_layout(user_id):
    main_layout = [
        loc(Lk.send_code, user_id),
        loc(Lk.raffle, user_id),
        loc(Lk.sell_tickets, user_id),
        loc(Lk.my_profile, user_id)
    ]
    return main_layout

def get_code_layout(user_id):
    code_layout = [
        "Roblox 200", "Roblox 400",
        "Roblox 800", "Roblox 1000",
        "Overwatch 200", "Overwatch 500",
        "Overwatch 1000", loc(Lk.back, user_id)
    ]
    return code_layout

def get_raffle_layout(user_id):
    raffle_layout = [
        f"{loc(Lk.raffle_100, user_id)}$",
        loc(Lk.back, user_id)
    ]
    return raffle_layout

def get_sell_layout(user_id):
    sell_layout = [
        loc(Lk.back, user_id)
    ]
    return sell_layout

def get_profile_layout(user_id):
    profile_layout = [
        loc(Lk.set_wallet, user_id),
        loc(Lk.set_r_code, user_id),
        loc(Lk.referral_code, user_id),
        loc(Lk.back, user_id)
    ]
    return profile_layout
