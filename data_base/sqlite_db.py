import sqlite3 as sq

"""Еван дб"""
def sql_start_evan():
    global base, cur
    base = sq.connect('serials.db')
    cur = base.cursor()
    if base:
        print('Data base connnected OK!')
    base.execute("CREATE TABLE IF NOT EXISTS serials_evan(user_id INTEGER, name_serial TEXT UNIQUE, season TEXT, series TEXT)")
    base.commit()


"""Рома дб"""
def sql_start_roma():
    global base, cur
    base = sq.connect('serials.db')
    cur = base.cursor()
    if base:
        print('Data base connnected OK!')
    base.execute("CREATE TABLE IF NOT EXISTS serials_roma(user_id INTEGER, name_serial TEXT UNIQUE, season TEXT, series TEXT)")
    base.commit()
    

"""Влад дб"""
def sql_start_vlad():
    global base, cur
    base = sq.connect('serials.db')
    cur = base.cursor()
    if base:
        print('Data base connnected OK!')
    base.execute("CREATE TABLE IF NOT EXISTS serials_vlad(user_id INTEGER, name_serial TEXT UNIQUE, season TEXT, series TEXT)")
    base.commit()
