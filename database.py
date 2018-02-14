import sqlite3
# import indices as metrics
# from decimal import *
# import sys
# sys.path.append("..")
# import timestamp as ts

lFtrCols = ["title","year", "runtimes","giant_cover_url","genres", 'color_info', 'director', 'cast_1st',
               'cast_2nd', 'cast_3rd', 'countries', 'languages', 'writer',
               'editor', 'cinematographer', 'art_director', 'costume_designer',
               'original_music', 'sound_mix', 'production_companies']

lLblCols = ["real_1", "real_2", "real_3", "real_4", "real_5", "real_6",
               "real_7", "real_8", "real_9", "real_10","o_predict_1","o_predict_2","o_predict_3", "o_predict_4", "o_predict_5", "o_predict_6",
                "o_predict_7", "o_predict_8", "o_predict_9", "o_predict_10"]

indexs=['cheby','clark','cbra','k-l','cos','intsc']


def connect_to_sql():
    global cur,conn
    try:
        conn = sqlite3.connect('movie.db') 
        cur = conn.cursor()
    except Exception as e:
        print (' - CONNECT_TO_SQL - An {} exception occured.'.format(e))
    

def get_instance_basic(mvID):
    global cur,conn
    # 0:id, 1:title, 2:cover,3:year
    cur.execute("SELECT title,cover_url,year FROM feature WHERE id=?",(mvID,))
    rst=cur.fetchone()
    entry=[]
    entry.append(mvID)
    entry.append(rst[0] )
    temp=rst[1]+""
    temp=temp[0:15]+"cn"+temp[17:len(temp)]
    entry.append(temp)
    entry.append(rst[2] )
    # rating = []
    # for col in lLblCols:
    #     cur.execute("SELECT %s FROM rating WHERE id =?"%col,(mvID,))
    #     rst=cur.fetchone()
    #     rating.append(int(rst[0]*10000))
    # entry.append(rating)
    # cur.execute("SELECT predict_time,predict_text FROM rating WHERE id =?",(mvID,))
    # rst=cur.fetchone()
    # entry.append(rst[0])
    # entry.append("https://app.originstamp.org/s/"+ts.sha(rst[1]))
    return entry 


def select_movie():
    global cur,conn
    connect_to_sql()
    lMv=[]
    cur.execute("SELECT id FROM feature WHERE for=?",("test",))
    # TODO: filte movie by year/category
    lRst=cur.fetchall()
    for i in lRst:
        lMv.append(get_instance_basic(i[0]))
    return lMv



def get_instance_details(mvID):
    global cur,conn
    connect_to_sql()
    movie=[]
    rating = []
    # rating_ = []
    for col in lLblCols:
        cur.execute("SELECT %s FROM rating WHERE id = %s" % (col,mvID))
        rst=cur.fetchone()
        rating.append(int(rst[0]*10000)/100)
        # rating_.append(rst[0])
    movie.append(rating)
    # cur.execute("SELECT predict_time,predict_text FROM rating WHERE id =?",(mvID,))
    # rst=cur.fetchone()
    # movie['predict_time']=rst[0]
    # movie['predict_text']=rst[1]
    # movie['verify_url']="https://app.originstamp.org/s/"+ts.sha(rst[1])
    # movie['sha256']=ts.sha(rst[1])
    # movie['metrics']=metrics.cal(rating_[10:20],rating_[0:10])


    for keyword in lFtrCols:
        cur.execute("SELECT %s FROM feature WHERE id= '%s'" % (keyword,str(mvID)))
        result = cur.fetchone()
        if keyword=="year" or keyword=="runtimes":
            if result[0]==0:
                movie.append('No information')
            else:
                movie.append(result[0])
        elif keyword =="giant_cover_url":
            temp=result[0]+""
            temp=temp[0:15]+"cn"+temp[17:len(temp)]
            movie.append(temp)
        else:
            templist=[]
            if result[0]=='':
                movie.append(['No information'])
            else:
                for value in result[0].split('$'):
                    if len(value.split('&'))>=2: 
                        templist.append(value.split('&')[1])
                    else:
                        templist.append(value)
                movie.append(templist)                    
        conn.commit()

    return movie


def perfect_prediction():
    global cur,conn
    connect_to_sql()
    movies=[]
    # TODO: order by metric
    cur.execute("SELECT %s FROM feature WHERE for='test' order by id " % 'id, title,giant_cover_url')
    result = cur.fetchall()
    for i in range(3):
        movies.append(result[i])
    cur.execute("SELECT %s FROM feature WHERE for='test' order by id " % 'id, title,cover_url')
    result = cur.fetchall()
    for i in range(6):
        movies.append(result[3+i])
    conn.commit()
    return movies

def recent_prediction():
    global cur,conn
    connect_to_sql()
    movies=[]
    # TODO: order by metric
    cur.execute("SELECT %s FROM feature WHERE for='test' order by id " % 'id, title,giant_cover_url')
    result = cur.fetchall()
    for i in range(3):
        movies.append(result[i])
    cur.execute("SELECT %s FROM feature WHERE for='test' order by id " % 'id, title,cover_url')
    result = cur.fetchall()
    for i in range(6):
        movies.append(result[3+i])
    conn.commit()
    return movies


# if __name__ == '__main__':
#     # print (select_movie())
#     # print (get_instance_details('3314958'))
#     # print (perfect_prediction())