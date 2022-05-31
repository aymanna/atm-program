import sqlite3
from datetime import datetime


path = 'pg.db'

def in_data(id: str) -> bool:
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute("SELECT id FROM users WHERE id = :id ;", {'id': id})
        ans = c.fetchone()
        conn.commit()
    
    if ans is None:
        return False
    return True


def get_user(id: str) -> tuple:
    if not in_data(id):
        raise Exception("the id is not within the database")
    
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute(f"SELECT * FROM users WHERE id = :id ;", {'id': id})
        ans = c.fetchone()
        conn.commit()

    return ans


def true_user(id: str, input_pin: str) -> bool:
    user_pin = get_user(id)[2]
    return input_pin == user_pin


def get_balance(id: str) -> int:
    user_balance = get_user(id)[3]
    return user_balance


def get_transactions(id: str) -> tuple:
    if not in_data(id):
        raise Exception("the target id is not within the database")
    
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute(
            """
            SELECT transactions.amount, transactions.description, transactions.date
            FROM transactions
            JOIN users
            ON transactions.id = users.id
            WHERE transactions.user_id = :id ;
            """,
            {'id': id}
        )
        ans = c.fetchall()
        conn.commit()
    return ans


def update_balance(balance: int, id: str) -> None:
    if not in_data(id):
        raise Exception("the target id is not within the database")
    
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET balance = :balance WHERE id = :id ;",
                  {'balance': balance, 'id': id})
        conn.commit()


def update_pin(pin: str, id: str) -> None:
    if not in_data(id):
        raise Exception("the target id is not within the database")
    
    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute("UPDATE users SET pin = :pin WHERE id = :id ;",
                  {'pin': pin, 'id': id})
        conn.commit()


def insert_transactions(id: str, amount: int, desc: str, target_id=None) -> None:
    if target_id is None:
        target_id = id

    if not (in_data(id) and in_data(target_id)):
        raise Exception("the id is not within the database")

    date = str(datetime.now())[:19].split(" ")[0]   # get current date

    with sqlite3.connect(path) as conn:
        c = conn.cursor()
        c.execute("INSERT INTO transactions VALUES (:id, :user_id, :amount, :desc, :date);",
                  {"id": target_id, "user_id": id, "amount": amount, "desc": desc, "date": date})
        conn.commit()
