#imports
import sqlite3
import numpy as np
import functools
import operator
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

#config
connection = sqlite3.connect("database/data", check_same_thread=False)
cursor = connection.cursor()


def initSession(u, p):
    allUser = cursor.execute("SELECT user FROM account;").fetchall()
    try:
        n = allUser.index((u,))
        Pass = cursor.execute(f"SELECT password FROM account WHERE user = '{u}';").fetchone()
        return check_password_hash(functools.reduce(operator.add, Pass), p)
    except:
        return False


def addValuesUser(u, e, p):
    if u != "" and e != "" and p != "":
        allUser = cursor.execute("SELECT user FROM account;").fetchall()
        allu = functools.reduce(operator.add, allUser)
        allmails = cursor.execute("SELECT email FROM account;").fetchall()
        allm = functools.reduce(operator.add, allmails)
        print(allm)
        if f'{u}' in allu or e in allm:
            return False
        else:
            time = datetime.now().date()
            cursor.execute(f"""INSERT INTO account VALUES (6,'{u}', '{e}', '{generate_password_hash(p)}', '{time}');""")
            connection.commit()
            return True
    else:
        return False


def changPassword(u, p):
    cursor.execute(f"UPDATE account SET password = '{generate_password_hash(p)}' WHERE user = '{u}';")
    connection.commit()
    return "i"


def getIcon(u):
    icon = cursor.execute(f"SELECT logo FROM account WHERE user = '{u}';").fetchone()
    return functools.reduce(operator.add, icon)


def changIcon(u, n):
    cursor.execute(f"UPDATE account SET logo = '{n}' WHERE user = '{u}';")
    connection.commit()
    return "i"


def getEmail(u):
    e = cursor.execute(f"SELECT email FROM account WHERE user = '{u}';").fetchone()
    return functools.reduce(operator.add, e)

def getDateCreate(n):
    date = cursor.execute(f"SELECT date FROM account WHERE user = '{n}'")
    return functools.reduce(operator.add, date)


def getDiscussion():
    old = []
    for i in np.unique(cursor.execute("SELECT ID FROM discussions ;").fetchall()):
        old.append(cursor.execute(f"""SELECT * FROM discussions WHERE ID = '{i}';""").fetchone())
    return old[::-1]


def getNDiscussions():
    n = []
    for i in np.unique(cursor.execute("SELECT ID FROM discussions;").fetchall()):
        n.append(len(functools.reduce(operator.add, cursor.execute(f"SELECT ID FROM discussions WHERE ID = '{i}';").fetchall())))
    return n


def getAllUsers():
    allUser = cursor.execute("SELECT user FROM account;").fetchall()
    g = functools.reduce(operator.add, allUser)
    return len(g)


def getEmailDiscussion(n):
    emails = []
    usuarios = np.unique(cursor.execute(f"SELECT user FROM discussions WHERE ID = '{n}';").fetchall())
    for i in usuarios:
        emails.append(functools.reduce(operator.add, cursor.execute(f"SELECT email FROM account WHERE user = '{i}';").fetchone()))
    return emails


def getAllDiscussion(n):
    all = cursor.execute(f"""SELECT * FROM discussions WHERE ID = '{n}';""").fetchall()
    return all

def getAllUserDiscussion(n):
    all = cursor.execute(f"""SELECT * FROM discussions WHERE user = '{n}'""").fetchall()
    return all


def getTopic(n):
    one = cursor.execute(f"""SELECT name FROM discussions WHERE ID = '{n}';""").fetchone()
    return one


def addComents(id, name, user, comment, date):
    cursor.execute(f"""INSERT INTO discussions
                                        VALUES ('{id}', '{name}', '{user}', '{comment}', '{date}')""")
    connection.commit()


def deletComent(n, c):
    cursor.execute(f"""DELETE FROM discussions WHERE ID = '{n}' AND comment = '{c}'""")
    connection.commit()
