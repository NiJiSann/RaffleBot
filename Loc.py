import csv

from telebot.types import *
import DataBase

loc_data = {}


def show_loc():
    kb = InlineKeyboardMarkup(row_width=1)
    eng_btn = InlineKeyboardButton(text=f"English", callback_data='eng')
    rus_btn = InlineKeyboardButton(text=f"Русский", callback_data='rus')
    uzb_btn = InlineKeyboardButton(text=f"Ozbek tili", callback_data='uzb')
    kb.add(eng_btn, rus_btn, uzb_btn)
    text = 'Choose language'
    return kb, text


def addNameToDictionary(d, tup):
    if tup[0] not in d:
        d[tup[0]] = {}
    d[tup[0]][tup[1]] = [tup[2]]


def parse_loc_keys():
    body = ''
    with open(f'loc.csv', mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)

        for code in csvFile:
            for lang in code:
                if lang == 'key':
                    continue
                text = f'{lang} = "{lang}"\n'
                body += text
            break

        for line in csvFile:
            key = line[0]
            text = f'{key} = "{key}"\n'
            body += text

    with open(f'LocKeys.py', mode='w', encoding='utf-8') as py:
        py.write(body)


def parse_loc():
    with open(f'loc.csv', mode='r', encoding='utf-8') as file:
        csvFile = csv.reader(file)
        codes = []

        for code in csvFile:
            for lang in code:
                if lang == 'key':
                    continue
                codes.append(lang)
            break

        for line in csvFile:
            key = line[0]
            for i in range(len(codes)):
                tup = (key, codes[i], line[i + 1])
                addNameToDictionary(loc_data, tup)


def get_loc(key, user_id):
    lang = DataBase.get_user_loc(user_id)
    if lang == 'None':
        lang = 'eng'
    try:
        return loc_data[key][lang][0]
    except Exception as e:
        print(e)

if __name__ == '__main__':
    pass
