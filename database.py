import sqlite3
# import indices as metrics
# from decimal import *
# import sys
# sys.path.append("..")
# import timestamp as ts

lFtrCols = ["title","year", "runtimes","giant_cover_url","genres", 'color_info', 'cast_1st',
               'cast_2nd', 'cast_3rd', 'countries', 'languages', 'director', 'writer','producer',
               'composers','editor' , 'art_director','cinematographer', 'costume_designer','production_companies']

lLblCols = ["real_1", "real_2", "real_3", "real_4", "real_5", "real_6",
               "real_7", "real_8", "real_9", "real_10","o_predict_1","o_predict_2","o_predict_3", "o_predict_4", "o_predict_5", "o_predict_6",
                "o_predict_7", "o_predict_8", "o_predict_9", "o_predict_10"]

# indexs=['cheby','clark','cbra','k-l','cos','intsc']


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
    i=temp.index('._V1')
    temp=temp[0:i]+'._V1_SY270_CR0,0,180,270_.jpg'
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
        cur.execute("SELECT %s FROM rating WHERE id = '%s'" % (col,mvID))
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
            if result[0]=='NULL':
                movie.append(['No information'])
            else:
                movie.append(result[0].split('$'))                      
        conn.commit()

    return movie


def perfect_prediction():
    global cur,conn
    connect_to_sql()
    movies=[]
    # TODO: db operation should be optimized.
    cur.execute("SELECT id FROM rating order by metric ")
    result = cur.fetchall()
    for i in range(3):
        entry=[]
        entry.append(result[i][0])
        cur.execute("SELECT title,giant_cover_url FROM feature WHERE id= '%s'" % result[i][0])
        r = cur.fetchone()
        entry.append(r[0])
        entry.append(r[1])
        movies.append(entry)
    for i in range(6):
        entry=[]
        entry.append(result[3+i][0])
        cur.execute("SELECT title,cover_url FROM feature WHERE id= '%s'" % result[3+i][0])
        r = cur.fetchone()
        entry.append(r[0])
        temp=r[1]+""
        temp=temp[0:15]+"cn"+temp[17:len(temp)]
        i=temp.index('._V1')
        temp=temp[0:i]+'._V1_SY300_CR0,0,200,300_.jpg'
        entry.append(temp)
        movies.append(entry)
    conn.commit()
    return movies


# TODO: order by date
def recent_prediction():
    global cur,conn
    connect_to_sql()
    movies=[]
    cur.execute("SELECT id FROM rating order by metric ")
    result = cur.fetchall()
    for i in range(3):
        entry=[]
        entry.append(result[i][0])
        cur.execute("SELECT title,giant_cover_url FROM feature WHERE id= %s" % result[i][0])
        r = cur.fetchone()
        entry.append(r[0])
        entry.append(r[1])
        movies.append(entry)

    cur.execute("SELECT %s FROM feature WHERE for='test' order by id " % 'id, title,cover_url')
    result = cur.fetchall()
    entry=[]
    for i in range(6):
        entry.clear()
        entry.append(rst[3+i][0] )
        entry.append(rst[3+i][1] )
        temp=rst[3+i][2]+""
        temp=temp[0:15]+"cn"+temp[17:len(temp)]
        i=temp.index('._V1')
        temp=temp[0:i]+'._V1._SX200_SY300_.jpg'
        entry.append(temp)
        movies.append(entry)
    conn.commit()
    return movies


# if __name__ == '__main__':
#     print (select_movie())
#     print (get_instance_details('3314958'))
#     print (perfect_prediction())