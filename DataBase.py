import sqlite3
import time


def create_table(drop, table):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    cursor.execute(drop)
    cursor.execute(table)
    connection.commit()
    connection.close()


def get_query_executor(query):
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        data = cursor.execute(query)
        res = data.fetchall()
        connection.commit()
        connection.close()
        return res
    except Exception as e:
        print(e)
        pass


def set_query_executor(query, params):
    try:
        connection = sqlite3.connect('users.db')
        cursor = connection.cursor()
        cursor.execute(query, params)
        cursor.fetchall()
        connection.commit()
        connection.close()
    except Exception as e:
        time.sleep(1)
        set_query_executor(query, params)
        print(e)
        pass


# region GET section
def get_user(user_id):
    query = f"SELECT * FROM USERS WHERE user_id = {user_id}"
    return get_query_executor(query)


def get_user_r_code(user_id):
    query = f"SELECT referral_own FROM USERS WHERE user_id = {user_id}"
    return get_query_executor(query)[0][0]


def get_user_wallet(user_id):
    query = f"SELECT wallet FROM USERS WHERE user_id = {user_id}"
    return get_query_executor(query)[0][0]


def get_user_name(user_id):
    query = f"SELECT user_name FROM USERS WHERE user_id = {user_id}"
    return get_query_executor(query)[0][0]


def get_user_ticket_count(user_id):
    query = f"SELECT tickets FROM USERS WHERE user_id = {user_id}"
    return get_query_executor(query)[0][0]


def get_user_loc(user_id):
    query = f"SELECT loc FROM USERS WHERE user_id = {user_id}"
    return get_query_executor(query)[0][0]


def get_user_reputation(user_id):
    query = f"SELECT reputation FROM USERS WHERE user_id = {user_id}"
    return get_query_executor(query)[0][0]


def get_user_f_r_code(user_id):
    query = f"SELECT referral_user FROM USERS WHERE user_id = {user_id}"
    return get_query_executor(query)[0][0]


def get_user_f_id(user_id):
    fr = get_user_f_r_code(user_id)
    query = f"SELECT user_id FROM USERS WHERE referral_own = {fr}"
    return get_query_executor(query)[0][0]


def get_code_quantity(user_id):
    query = f"SELECT quantity_of_codes FROM USERS WHERE user_id = {user_id}"
    return get_query_executor(query)[0][0]


def get_codes(denied, checking, confirmed):
    where = ''
    if denied:
        where += 'WHERE status = "denied" '
    if checking:
        if not denied:
            where += 'WHERE '
        else:
            where += 'OR '
        where += 'status = "checking" '
    if confirmed:
        if not checking and not denied:
            where += 'WHERE '
        else:
            where += 'OR '
        where += 'status = "confirmed" '
    query = f'''SELECT * FROM CODES {where}'''

    return get_query_executor(query)


def get_payouts(unpaid):
    where = ''
    if unpaid:
        where += 'WHERE status = "unpaid" '
    query = f'''SELECT * FROM PAYOUT {where}'''

    return get_query_executor(query)


def get_raffle100():
    query = f"SELECT * FROM RAFFLE100"
    return get_query_executor(query)


def get_users(column):
    query = f"SELECT {column} FROM USERS"
    return get_query_executor(query)


# endregion

# region SET section
def set_user(name, user_id, referral, name_last=None, username=None):
    query = '''INSERT INTO USERS (name, name_last, user_id, referral_own, user_name) VALUES(?,?,?,?,?)'''
    params = (name, name_last, user_id, referral, username)
    set_query_executor(query, params)


def set_code(user_id, code, img):
    query = '''INSERT INTO CODES(user_name, user_id, code, img) VALUES(?,?,?,?)'''
    params = (get_user_name(user_id), user_id, code, img)
    set_query_executor(query, params)


def set_payout(user_id, tickets):
    query = '''INSERT INTO PAYOUT(user_id, tickets, wallet, status) VALUES(?,?,?,?)'''
    wallet = get_user_wallet(user_id)
    params = (user_id, tickets, wallet, 'unpaid')
    set_query_executor(query, params)


def set_raffle_p(user_id):
    query = '''INSERT INTO RAFFLE100(user_id, wallet) VALUES(?,?)'''
    wallet = get_user_wallet(user_id)
    params = (user_id, wallet)
    set_query_executor(query, params)


def set_wallet(user_id, wallet):
    query = f'''UPDATE USERS SET wallet=? WHERE user_id=?'''
    params = (wallet, user_id)
    set_query_executor(query, params)


def set_friend_referral(user_id, code):
    query = f'''UPDATE USERS SET referral_user=? WHERE user_id=?'''
    params = (code, user_id)
    set_query_executor(query, params)


def set_user_ticket_count(user_id, amount):
    query = '''UPDATE USERS SET tickets=? WHERE user_id=?'''
    params = (amount, user_id)
    set_query_executor(query, params)


def set_user_loc(user_id, loc):
    query = f'''UPDATE USERS SET loc=? WHERE user_id=?'''
    params = (loc, user_id)
    set_query_executor(query, params)


def set_code_state(user_id, state):
    query = f'''UPDATE CODES SET status=? WHERE user_id=?'''
    params = (state, user_id)
    set_query_executor(query, params)


def set_payout_state(user_id, state):
    query = f'''UPDATE PAYOUT SET status=? WHERE user_id=?'''
    params = (state, user_id)
    set_query_executor(query, params)


def add_reputation(user_id, val):
    query = f'''UPDATE USERS SET reputation=? WHERE user_id=?'''
    rep = get_user_reputation(user_id) + val
    params = (rep, user_id)
    set_query_executor(query, params)


def add_tickets(user_id, val):
    query = f'''UPDATE USERS SET tickets=? WHERE user_id=?'''
    rep = get_user_ticket_count(user_id) + val
    params = (rep, user_id)
    set_query_executor(query, params)


def add_code_quantity(user_id, val):
    query = f'''UPDATE USERS SET quantity_of_codes=? WHERE user_id=?'''
    rep = get_code_quantity(user_id) + val
    params = (rep, user_id)
    set_query_executor(query, params)


def add_r_tickets(user_id):
    query = f'''UPDATE USERS SET tickets=? WHERE user_id=?'''
    f_id = get_user_f_id(user_id)
    t = get_user_ticket_count(f_id) + 1
    params = (t, f_id)
    set_query_executor(query, params)


# endregion

def create_code_tb():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS CODES")

    # Creating table
    table = """ CREATE TABLE CODES(
                 user_name VARCHAR(255),
                 user_id INT,
                 code VARCHAR(255),
                 img BLOB,
                 status VARCHAR(255)
             ); """

    cursor.execute(table)
    connection.commit()
    connection.close()


def create_users_tb():
    drop = "DROP TABLE IF EXISTS USERS"
    table = """ CREATE TABLE USERS(
                name VARCHAR(255),
                name_last VARCHAR(255),
                user_name VARCHAR(255),
                reputation INT DEFAULT 0,
                user_id INT,
                referral_own VARCHAR(255),
                referral_user VARCHAR(255),
                tickets INT DEFAULT 0,
                quantity_of_codes INT DEFAULT 0,
                wallet VARCHAR(255),
                loc VARCHAR(255)
            ); """

    create_table(drop, table)


def create_raffle100_tb():
    drop = "DROP TABLE IF EXISTS RAFFLE100"
    table = """ CREATE TABLE RAFFLE100(
                user_id INT,
                wallet VARCHAR(255)
            ); """
    create_table(drop, table)


def create_payout_tb():
    drop = "DROP TABLE IF EXISTS PAYOUT"
    table = """ CREATE TABLE PAYOUT(
                user_id INT,
                tickets INT DEFAULT 0,
                wallet VARCHAR(255),
                status VARCHAR(255)
            ); """
    create_table(drop, table)


if __name__ == "__main__":
    create_users_tb()
    create_code_tb()
    create_payout_tb()
    create_raffle100_tb()
    pass
