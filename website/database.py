import numpy as np
import scipy.io as sio
import MySQLdb

#SQL variables
mysql_ip = 'localhost'
mysql_user = 'root'
mysql_passwd = 'root'
mysql_db = 'mv'
cur=None
conn=None


info_cols=['title','cover_url','year','runtimes','genres','color_info','director','cast_1','cast_2','cast_3','countries','languages',
'writer','editor','cinematographer','art_direction','costume_designer','original_music','sound_mix',
'production_companies']

rating_cols=['number_of_votes_1','number_of_votes_2','number_of_votes_3',
'number_of_votes_4','number_of_votes_5','number_of_votes_6','number_of_votes_7','number_of_votes_8',
'number_of_votes_9','number_of_votes_10']





def connect_to_sql():
    global cur,conn
    try:
        conn = MySQLdb.connect(mysql_ip, mysql_user, mysql_passwd, mysql_db, charset='utf8')
        cur = conn.cursor()
        print ' - CONNECT_TO_SQL - Connect successfully.'
    except Exception as e:
        print ' - CONNECT_TO_SQL - An {} exception occured.'.format(e)

def get_instance_basic(table):
    connect_to_sql()
    if table=='new_movies':
        data=sio.loadmat('o_movieDataSet.mat')
        distr=sio.loadmat('o_predictDistribution.mat')
        distr['preDistribution']
        templist=[]
        for i in data['testIndex'][0]:
            entry=[]
            cur.execute("SELECT id,title,cover_url,year FROM %s LIMIT %s,1;" % (table,i))
            result = cur.fetchone()
            entry.append(result[0])
            entry.append(result[1]+'-%d' % result[3])
            entry.append(result[2])
            templist.append(entry)
            #print distr['preDistribution'][j]
        # print templist
        return templist  

    elif table =='future_movies':
        cur.execute("SELECT id,title,cover_url,year FROM %s;" % table)
        result = cur.fetchall()
        templist=[]
        for i in result:
            entry=[]
            entry.append(i[0])
            entry.append(i[1]+'-%d' % i[3])
            entry.append(i[2])
            templist.append(entry)
        # print templist
        return templist 


def get_instance_details(table,id):
    connect_to_sql()
    movie={}
    if table=='new_movies':
        data=sio.loadmat('o_movieDataSet.mat')
        distr=sio.loadmat('o_predictDistribution.mat')
        distr['preDistribution']
        movie_rating=[]
        for i in data['testIndex'][0]:
            entry=[]
            cur.execute("SELECT id,title,cover_url,year FROM %s LIMIT %s,1;" % (table,i))
            result = cur.fetchone()
            #print distr['preDistribution'][j]

        for keyword in info_cols:
            cur.execute("SELECT %s FROM new_movies WHERE id= '%s'" % (keyword,str(id)))
            result = cur.fetchone()
            if keyword=="year" or keyword=="runtimes":
                movie[keyword]=result[0]
            else:
                templist=[]
                if result[0]=='':
                    movie[keyword]='No information'
                else:
                    for value in result[0].split('$'):
                        # if len(value.split('&'))>=2: 
                        #     templist.append(value.split('&')[1])
                        # else:
                        #     templist.append(value)
                        templist.append(value)
                    movie[keyword]=templist                    
            conn.commit()
        for keyword in rating_cols:
            cur.execute("SELECT %s FROM new_movies WHERE id= '%s'" % (keyword,str(id)))
            result = cur.fetchone()
            rating_sum=rating_sum+float(result[0])
            movie_rating.append(float(result[0]))
            conn.commit()
        for i in xrange(0,len(movie_rating)):
            movie[rating_cols[i]]=movie_rating[i]/rating_sum 
        print movie
        return movie

    elif table =='future_movies':
        distr=sio.loadmat('f_predictDistribution.mat')
        for keyword in info_cols:
            cur.execute("SELECT %s FROM future_movies WHERE id= '%s'" % (keyword,str(id)))
            result = cur.fetchone()
            conn.commit()
            if keyword=="year" or keyword=="runtimes":
                movie[keyword]=result[0]
            else:
                templist=[]
                if result[0]=='':
                    movie[keyword]='No information'
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
        for i in xrange(0,10):
            movie['f_'+rating_cols[i]]=distr['preDistribution'][index][i]

        # print movie
        return movie
        



if __name__ == '__main__':
    get_instance_details('future_movies','5362988')





