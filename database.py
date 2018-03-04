import pymysql
import time
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
        conn = pymysql.connect(host='movie-data.ch6y02vfazod.ap-northeast-1.rds.amazonaws.com',
                             user='admin',
                             password='movierating123',
                             database='movierating',
                             port=3306,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
    except Exception as e:
        print (' - CONNECT_TO_SQL - An {} exception occured.'.format(e))
    

def get_instance_basic(mvID):
    global cur,conn
    # 0:id, 1:title, 2:cover,3:year
    cur.execute("SELECT `title`,`cover_url`,`year` FROM `data` WHERE `id`=%s;",(mvID,))
    rst=cur.fetchone()
    entry=[]
    entry.append(mvID)
    entry.append(rst['title'] )
    temp=rst['cover_url']+""
    temp=temp[0:15]+"cn"+temp[17:len(temp)]
    i=temp.index('._V1')
    temp=temp[0:i]+'._V1_SY270_CR0,0,180,270_.jpg'
    entry.append(temp)
    entry.append(rst['year'] )
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
    lMv=[]
    cur.execute("SELECT `id` FROM `data` WHERE `for`='test';")
    # TODO: filte movie by year/category
    lRst=cur.fetchall()
    for i in lRst:
        lMv.append(get_instance_basic(i['id']))
    conn.close()
    return lMv



def get_instance_details(mvID):
    global cur,conn
    movie=[]
    rating = []
    # rating_ = []
    cur.execute("SELECT `real_1`, `real_2`, `real_3`, `real_4`, `real_5`, `real_6`, `real_7`, `real_8`, `real_9`, `real_10`, `o_predict_1`, `o_predict_2`, `o_predict_3`, `o_predict_4`, `o_predict_5`, `o_predict_6`, `o_predict_7`, `o_predict_8`, `o_predict_9`, `o_predict_10` FROM `data` WHERE `id` = %s;",mvID)
    rst=cur.fetchone()
    for col in lLblCols:
        rating.append(int(rst[col]*10000)/100)
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
        cur.execute("SELECT `%s` FROM `data` WHERE `id`= %s;" % (keyword,str(mvID)))
        result = cur.fetchone()
        if keyword=="year" or keyword=="runtimes":
            if result[keyword]==0:
                movie.append('No information')
            else:
                movie.append(result[keyword])
        elif keyword =="giant_cover_url":
            temp=result["giant_cover_url"]+""
            temp=temp[0:15]+"cn"+temp[17:len(temp)]
            movie.append(temp)
        else:
            templist=[]
            if result[keyword]=='NULL':
                movie.append(['No information'])
            else:
                movie.append(result[keyword].split('$'))                      
    conn.close()

    return movie


def perfect_prediction():
    global cur,conn
    movies=[]
    # TODO: db operation should be optimized.
    cur.execute("SELECT `id` FROM `data` WHERE `for` = 'test' order by `metric`;")
    result = cur.fetchall()
    for i in range(3):
        entry=[]
        entry.append(result[i]['id'])
        cur.execute("SELECT `title`,`giant_cover_url` FROM `data` WHERE `id`= %s;" % result[i]['id'])
        r = cur.fetchone()
        entry.append(r['title'])
        entry.append(r['giant_cover_url'])
        movies.append(entry)
    for i in range(6):
        entry=[]
        entry.append(result[3+i]['id'])
        cur.execute("SELECT `title`,`cover_url` FROM `data` WHERE `id`= %s;" % result[3+i]['id'])
        r = cur.fetchone()
        entry.append(r['title'])
        temp=r['cover_url']+""
        temp=temp[0:15]+"cn"+temp[17:len(temp)]
        i=temp.index('._V1')
        temp=temp[0:i]+'._V1_SY300_CR0,0,200,300_.jpg'
        entry.append(temp)
        movies.append(entry)
    return movies


# TODO: order by date
def recent_prediction():
    global cur,conn
    # for official version
    # year = time.localtime(time.time())[0]
    # month = time.localtime(time.time())[1]
    # date = []
    # for i in range(3):
    #     if month is not 1:
    #         month -=1
    #     else:
    #         month =12
    #         year -=1
    #     date.append((year,month))
    date = [(2017,11),(2017,10),(2017,9)]
    movies=[]
    for (year,month) in date:
        cur.execute("SELECT `id`,`title` FROM `data` WHERE `for`='test' and `year`=%d and `month` = %d;" % (year,month))
        rst=cur.fetchmany(4)
        for mv in rst:
            mv['date']='%d-%02d' % (year, month)
            movies.append(mv)
    conn.close()

    return movies


# if __name__ == '__main__':
    # print (select_movie())
    # print (get_instance_details('3314958'))
    # print (perfect_prediction())
    # connect_to_sql()
    # print (recent_prediction())