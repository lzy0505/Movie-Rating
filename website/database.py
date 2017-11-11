import numpy as np
import scipy.io as sio
import sqlite3
import indexs as indexs_cal
from decimal import *

lFtrCols=['title','cover_url','year','runtimes','genres','color_info','director','cast_1','cast_2','cast_3','countries','languages',
'writer','editor','cinematographer','art_direction','costume_designer','original_music','sound_mix',
'production_companies']

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
    print rst
    entry.append(rst[0])
    entry.append(rst[1])
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
    connect_to_sql()
    getcontext().prec = 5
    movie={}
    if table=='new_movies':

        movie_rating=[]

        for keyword in lFtrCols:
            cur.execute("SELECT %s FROM new_movies WHERE id= '%s'" % (keyword,str(id)))
            result = cur.fetchone()
            if keyword=="year" or keyword=="runtimes":
                movie[keyword]=result[0]
            elif keyword =="cover_url":
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
        rating_sum=0
        for keyword in lLblCols:
            cur.execute("SELECT %s FROM new_movies WHERE id= '%s'" % (keyword,str(id)))
            result = cur.fetchone()
            rating_sum=rating_sum+float(result[0])
            movie_rating.append(float(result[0]))
            conn.commit()
        for i in xrange(0,len(movie_rating)):
            movie_rating[i]/=rating_sum
            movie['r_'+lLblCols[i]]=int(movie_rating[i]*10000)

        cur.execute("SELECT id FROM new_movies;")
        result = cur.fetchall()
        conn.commit()
        index=0
        for m in result:
            if m[0]== id:
                break
            index+=1
        for i in xrange(0,len(data['testIndex'][0])):
            if index == data['testIndex'][0][i]:
                index= i

        for i in xrange(0,10):
            movie['p_'+lLblCols[i]]=int(o_l_distr['preDistribution'][index][i]*10000)
            movie['b_p_'+lLblCols[i]]=int(o_b_distr['preDistribution'][index][i]*10000)
        result_index=indexs_cal.cal(movie_rating,o_l_distr['preDistribution'][index])
        for ind in indexs:
            movie['l_'+ind]=result_index[ind]
        result_index=indexs_cal.cal(movie_rating,o_b_distr['preDistribution'][index])
        for ind in indexs:
            if ind=='cos' or ind=='intsc':
                if float(movie['l_'+ind])>float(result_index[ind]):
                    movie["better_"+ind]=1
                elif float(movie['l_'+ind])<float(result_index[ind]):
                    movie["better_"+ind]=-1
                else:
                    movie["better_"+ind]=0
            else:
                if float(movie['l_'+ind])<float(result_index[ind]):
                    movie["better_"+ind]=1
                elif float(movie['l_'+ind])>float(result_index[ind]):
                    movie["better_"+ind]=-1
                else:
                    movie["better_"+ind]=0
            movie['b_'+ind]=result_index[ind]
        return movie

    # elif table =='future_movies':
    #     for keyword in lFtrCols:
    #         cur.execute("SELECT %s FROM future_movies WHERE id= '%s'" % (keyword,str(id)))
    #         result = cur.fetchone()
    #         conn.commit()
    #         if keyword=="year" or keyword=="runtimes":
    #             movie[keyword]=result[0]
    #         elif keyword =="cover_url":
    #             temp=result[0]+""
    #             movie[keyword]=temp[0:15]+"cn"+temp[17:len(temp)]
    #         else:
    #             templist=[]
    #             if result[0]=='':
    #                 movie[keyword]='-'
    #             else:
    #                 for value in result[0].split('$'):
    #                     if len(value.split('&'))>=2: 
    #                         templist.append(value.split('&')[1])
    #                     else:
    #                         templist.append(value)
    #                     # templist.append(value)
    #                 movie[keyword]=templist                    
    #         conn.commit()    
    #     cur.execute("SELECT id FROM future_movies;")
    #     result = cur.fetchall()
    #     conn.commit()
    #     index=0
    #     for m in result:
    #         if m[0]== id:
    #             break
    #         index+=1
    #     score=0.0
    #     rank=0
    #     for i in xrange(0,10):
    #         score+=((i+1)*f_b_distr['preDistribution'][index][i])
    #         movie['f_'+lLblCols[i]]=int(f_l_distr['preDistribution'][index][i]*10000)
    #         movie['b_f_'+lLblCols[i]]=int(f_b_distr['preDistribution'][index][i]*10000)
    #     for m in o_score:
    #         if score>m:
    #             rank+=1
    #     movie['rank']=int(rank/float(len(o_score))*100)
    #     # print movie
    #     return movie
        



if __name__ == '__main__':
    print get_instance_basic('3103166')





