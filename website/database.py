import numpy as np
import scipy.io as sio
import MySQLdb
import indexs as indexs_cal
from decimal import *
#SQL variables
mysql_ip = 'localhost'
mysql_user = 'root'
mysql_passwd = 'root'
mysql_db = 'mv'
cur=None
conn=None

data=None
o_l_distr=None
o_b_distr=None
f_l_distr=None
f_b_distr=None

o_score=[]

info_cols=['title','cover_url','year','runtimes','genres','color_info','director','cast_1','cast_2','cast_3','countries','languages',
'writer','editor','cinematographer','art_direction','costume_designer','original_music','sound_mix',
'production_companies']

rating_cols=['number_of_votes_1','number_of_votes_2','number_of_votes_3',
'number_of_votes_4','number_of_votes_5','number_of_votes_6','number_of_votes_7','number_of_votes_8',
'number_of_votes_9','number_of_votes_10']

indexs=['cheby','clark','cbra','k-l','cos','intsc']

def init():
    global o_score,data,o_l_distr,o_b_distr,f_l_distr,f_b_distr
    data=sio.loadmat('o_movieDataSet.mat')
    o_l_distr=sio.loadmat('o_predictDistribution.mat')
    o_b_distr=sio.loadmat('b_o_predictDistribution.mat')
    f_l_distr=sio.loadmat('f_predictDistribution.mat')
    f_b_distr=sio.loadmat('b_f_predictDistribution.mat')
    for m in data['trainDistribution']:
        score=0.0
        for i in xrange(0,10):
            score+=((i+1)*m[i])
        o_score.append(score)
    for m in data['testDistribution']:
        score=0.0
        for i in xrange(0,10):
            score+=((i+1)*m[i])
        o_score.append(score)



def connect_to_sql():
    global cur,conn,f_score
    try:
        conn = MySQLdb.connect(mysql_ip, mysql_user, mysql_passwd, mysql_db, charset='utf8')
        cur = conn.cursor()
    except Exception as e:
        print ' - CONNECT_TO_SQL - An {} exception occured.'.format(e)
    

def get_instance_basic(table):
    global data
    connect_to_sql()
    if table=='new_movies':
        templist=[]
        for i in data['testIndex'][0]:
            entry=[]
            cur.execute("SELECT id,title,cover_url,year FROM %s LIMIT %s,1;" % (table,i))
            result = cur.fetchone()
            entry.append(result[0])
            entry.append(result[1]+'-%d' % result[3])
            temp=result[2]+""
            temp=temp[0:15]+"cn"+temp[17:len(temp)]
            entry.append(temp)
            templist.append(entry)
        return templist  

    elif table =='future_movies':
        cur.execute("SELECT id,title,cover_url,year FROM %s;" % table)
        result = cur.fetchall()
        templist=[]
        for i in result:
            entry=[]
            entry.append(i[0])
            entry.append(i[1]+'-%d' % i[3])
            temp=i[2]+""
            temp=temp[0:15]+"cn"+temp[17:len(temp)]
            entry.append(temp)
            templist.append(entry)
        # print templist

    
        return templist 


def get_instance_details(table,id):
    global data,o_l_distr,o_b_distr,f_l_distr,f_b_distr,o_score
    connect_to_sql()
    getcontext().prec = 5
    movie={}
    if table=='new_movies':

        movie_rating=[]

        for keyword in info_cols:
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
        for keyword in rating_cols:
            cur.execute("SELECT %s FROM new_movies WHERE id= '%s'" % (keyword,str(id)))
            result = cur.fetchone()
            rating_sum=rating_sum+float(result[0])
            movie_rating.append(float(result[0]))
            conn.commit()
        for i in xrange(0,len(movie_rating)):
            movie_rating[i]/=rating_sum
            movie['r_'+rating_cols[i]]=int(movie_rating[i]*10000)

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
            movie['p_'+rating_cols[i]]=int(o_l_distr['preDistribution'][index][i]*10000)
            movie['b_p_'+rating_cols[i]]=int(o_b_distr['preDistribution'][index][i]*10000)
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

    elif table =='future_movies':
        for keyword in info_cols:
            cur.execute("SELECT %s FROM future_movies WHERE id= '%s'" % (keyword,str(id)))
            result = cur.fetchone()
            conn.commit()
            if keyword=="year" or keyword=="runtimes":
                movie[keyword]=result[0]
            elif keyword =="cover_url":
                temp=result[0]+""
                movie[keyword]=temp[0:15]+"cn"+temp[17:len(temp)]
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
                        # templist.append(value)
                    movie[keyword]=templist                    
            conn.commit()    
        cur.execute("SELECT id FROM future_movies;")
        result = cur.fetchall()
        conn.commit()
        index=0
        for m in result:
            if m[0]== id:
                break
            index+=1
        score=0.0
        rank=0
        for i in xrange(0,10):
            score+=((i+1)*f_b_distr['preDistribution'][index][i])
            movie['f_'+rating_cols[i]]=int(f_l_distr['preDistribution'][index][i]*10000)
            movie['b_f_'+rating_cols[i]]=int(f_b_distr['preDistribution'][index][i]*10000)
        for m in o_score:
            if score>m:
                rank+=1
        movie['rank']=int(rank/float(len(o_score))*100)
        # print movie
        return movie
        



if __name__ == '__main__':
    get_instance_details('new_movies','0479997')





