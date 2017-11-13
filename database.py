import numpy as np
import scipy.io as sio
import sqlite3
import indices as metrics
from decimal import *
import data.timestamp as ts

lFtrCols = ["title","year", "runtimes","giant_cover_url","genres", 'color_info', 'director', 'cast_1st',
               'cast_2nd', 'cast_3rd', 'countries', 'languages', 'writer',
               'editor', 'cinematographer', 'art_director', 'costume_designer',
               'original_music', 'sound_mix', 'production_companies']

lLblCols = ["real_1", "real_2", "real_3", "real_4", "real_5", "real_6",
               "real_7", "real_8", "real_9", "real_10","predict_1","predict_2","predict_3", "predict_4", "predict_5", "predict_6",
                "predict_7", "predict_8", "predict_9", "predict_10"]

indexs=['cheby','clark','cbra','k-l','cos','intsc']


def connect_to_sql():
    global cur,conn
    try:
        conn = sqlite3.connect('movie.db') 
        cur = conn.cursor()
    except Exception as e:
        print ' - CONNECT_TO_SQL - An {} exception occured.'.format(e)
    

def get_instance_basic(mvID):
    global cur,conn
    connect_to_sql()
    cur.execute("SELECT title,cover_url,year FROM feature WHERE id=?",(mvID,))
    rst=cur.fetchone()
    entry=[]
    entry.append(mvID)
    entry.append(rst[0]+'-%d' % rst[2])
    temp=rst[1]+""
    temp=temp[0:15]+"cn"+temp[17:len(temp)]
    entry.append(temp)
    rating = []
    for col in lLblCols:
        cur.execute("SELECT %s FROM rating WHERE id =?"%col,(mvID,))
        rst=cur.fetchone()
        rating.append(int(rst[0]*10000))
    entry.append(rating)
    cur.execute("SELECT predict_time,predict_text FROM rating WHERE id =?",(mvID,))
    rst=cur.fetchone()
    entry.append(rst[0])
    entry.append("https://app.originstamp.org/s/"+ts.sha(rst[1]))
    return entry 


def select_movie():
    global cur,conn
    connect_to_sql()
    lMv=[]
    cur.execute("SELECT id FROM feature WHERE type=?",("predicted",))
    lRst=cur.fetchall()
    for i in lRst:
        lMv.append(get_instance_basic(i[0]))
    return lMv



def get_instance_details(mvID):
    global cur,conn
    connect_to_sql()
    movie={}
    movie_rating=[]
    for keyword in lFtrCols:
        cur.execute("SELECT %s FROM feature WHERE id= '%s'" % (keyword,str(mvID)))
        result = cur.fetchone()
        if keyword=="year" or keyword=="runtimes":
            if result[0]==0:
                movie[keyword]='No information'
            else:
                movie[keyword]=result[0]
        elif keyword =="giant_cover_url":
            temp=result[0]+""
            temp=temp[0:15]+"cn"+temp[17:len(temp)]
            movie[keyword]=temp
        else:
            templist=[]
            if result[0]=='':
                movie[keyword]='-'
            else:
                for value in result[0].split('$'):
                    if len(value.split('&'))>=2: 
                        templist.append(value.split('&')[1])
                    else:
                        templist.append(value)
                movie[keyword]=templist                    
        conn.commit()

    rating = []
    rating_ = []
    for col in lLblCols:
        cur.execute("SELECT %s FROM rating WHERE id =?"%col,(mvID,))
        rst=cur.fetchone()
        rating.append(int(rst[0]*10000))
        rating_.append(rst[0])
    movie['rating']=rating
    cur.execute("SELECT predict_time,predict_text FROM rating WHERE id =?",(mvID,))
    rst=cur.fetchone()
    movie['predict_time']=rst[0]
    movie['predict_text']=rst[1]
    movie['verify_url']="https://app.originstamp.org/s/"+ts.sha(rst[1])
    movie['sha256']=ts.sha(rst[1])
    movie['metrics']=metrics.cal(rating_[10:20],rating_[0:10])

    return movie



if __name__ == '__main__':
    print get_instance_details('3231054')





