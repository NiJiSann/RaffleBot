import sqlite3

def get_user(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query = f"SELECT * FROM USERS WHERE user_id = {user_id}"
    try:
        cursor.execute(query)
        res = cursor.fetchall()
    except:
        return 'Error'

    connection.close()
    return res

def set_user(name, user_id, referral, name_last=None, username=None):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query = '''INSERT INTO USERS (ID, name, name_last, user_id, referral_own, user_name) VALUES(?,?,?,?,?,?)'''
    query_len = '''SELECT * FROM USERS'''
    data = cursor.execute(query_len)
    length = len(data.fetchall())
    print(length)
    try:
        cursor.execute(query, (length+1, name, name_last, user_id, referral, username))
        cursor.fetchall()
        connection.commit()
    except Exception as e:
        print(e)

    connection.close()

def get_user_referr(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query = f"SELECT referral_own FROM USERS WHERE user_id = {user_id}"

    try:
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
        return data
    except Exception as e:
        print(e)
        connection.close()
        return ""

def get_user_name(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query = f"SELECT user_name FROM USERS WHERE user_id = {user_id}"

    try:
        cursor.execute(query)
        data = cursor.fetchall()
        connection.close()
        return data
    except Exception as e:
        print(e)
        connection.close()
        return ""

def add_code(user_id, code, img):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query = '''INSERT INTO CODES(ID, user_name, user_id, code, img) VALUES(?,?,?,?,?)'''
    query_len = '''SELECT * FROM CODES'''
    data = cursor.execute(query_len)
    length = len(data.fetchall())
    try:
        cursor.execute(query, (length+1, get_user_name(user_id)[0][0], user_id, code, img))
        cursor.fetchall()
        connection.commit()
    except Exception as e:
        print(e)

    connection.close()

def set_wallet(user_id, wallet):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query = f'''UPDATE USERS SET wallet=? WHERE user_id=?'''
    try:
        cursor.execute(query, (wallet, user_id))
        cursor.fetchall()
        connection.commit()
    except Exception as e:
        print(e)

    connection.close()

def set_friend_referral(user_id, code):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query = f'''UPDATE USERS SET referral_user=? WHERE user_id=?'''
    try:
        cursor.execute(query, (code, user_id))
        cursor.fetchall()
        connection.commit()
    except Exception as e:
        print(e)

    connection.close()

def get_raffle100_p_count():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query_len = '''SELECT * FROM RAFFLE100'''
    data = cursor.execute(query_len)
    length = len(data.fetchall())
    connection.commit()
    connection.close()
    return length

def get_user_ticket_count(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query = f"SELECT tickets FROM USERS WHERE user_id = {user_id}"
    data = cursor.execute(query)
    count = data.fetchall()[0][0]
    connection.commit()
    connection.close()
    return count

def get_user_loc(user_id):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query = f"SELECT loc FROM USERS WHERE user_id = {user_id}"
    data = cursor.execute(query)
    loc = data.fetchall()[0][0]
    connection.commit()
    connection.close()
    return loc

def get_codes(denied, checking, confirmed):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

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
    data = cursor.execute(query)
    res = data.fetchall()
    connection.commit()
    connection.close()
    return res

def set_user_ticket_count(user_id, amount):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query = '''UPDATE USERS SET tickets=? WHERE user_id=?'''
    cursor.execute(query, (amount, user_id))
    connection.commit()
    connection.close()

def set_user_loc(user_id, loc):
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()
    query = f'''UPDATE USERS SET loc=? WHERE user_id=?'''
    cursor.execute(query, (loc, user_id))
    connection.commit()
    connection.close()


def create_code_tb():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS CODES")

    # Creating table
    table = """ CREATE TABLE CODES(
                 ID INT PRIMARY KEY NOT NULL,
                 user_name VARCHAR(255),
                 user_id INT,
                 code VARCHAR(255),
                 img VARCHAR(255),
                 status VARCHAR(255)
             ); """

    cursor.execute(table)
    connection.commit()
    connection.close()
def create_users_tb():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS USERS")

    # Creating table
    table = """ CREATE TABLE USERS(
                ID INT PRIMARY KEY NOT NULL,
                name VARCHAR(255),
                name_last VARCHAR(255),
                user_name VARCHAR(255),
                reputation INT DEFAULT 0,
                user_id INT,
                referral_own VARCHAR(255),
                referral_user VARCHAR(255),
                tickets INT DEFAULT 0,
                quantity_of_codes INT,
                wallet VARCHAR(255),
                loc VARCHAR(255)
            ); """

    cursor.execute(table)
    connection.commit()
    connection.close()
def create_raffle100_tb():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS RAFFLE100")

    # Creating table
    table = """ CREATE TABLE RAFFLE100(
                user_id REAL,
                wallet VARCHAR(255)
            ); """

    cursor.execute(table)
    connection.commit()
    connection.close()
def create_payout_tb():
    connection = sqlite3.connect('users.db')
    cursor = connection.cursor()

    cursor.execute("DROP TABLE IF EXISTS PAYOUT")

    # Creating table
    table = """ CREATE TABLE PAYOUT(
                user_id REAL,
                tickets INT DEFAULT 0,
                wallet VARCHAR(255)
            ); """

    cursor.execute(table)
    connection.commit()
    connection.close()

if __name__ == "__main__":
    create_code_tb()
    create_users_tb()
