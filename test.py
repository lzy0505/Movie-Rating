# -*- coding:utf-8 -*-
import sqlite3

def func(mvID):
    try:
		conn = sqlite3.connect('movie.db') 
		cur = conn.cursor()
    except Exception as e:
        print ' - CONNECT_TO_SQL - An {} exception occured.'.format(e)
    cur.execute("SELECT title,cover_url,year FROM feature WHERE id=%s"%mvID)
    rst=cur.fetchone()


if __name__ == '__main__':
    func("3103166")
