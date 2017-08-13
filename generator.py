import MySQLdb
from movie import Movie
#SQL variables
mysql_ip = 'localhost'
mysql_user = 'root'
mysql_passwd = 'root'
mysql_db = 'mv'
cur=None
conn=None

info_cols=['year','runtimes','genres','color_info','director','cast_1','cast_2','cast_3','countries','languages',
'writer','editor','cinematographer','art_direction','costume_designer','original_music','sound_mix',
'production_companies']
rating_cols=['number_of_votes_1','number_of_votes_2','number_of_votes_3',
'number_of_votes_4','number_of_votes_5','number_of_votes_6','number_of_votes_7','number_of_votes_8',
'number_of_votes_9','number_of_votes_10']

#threshold=[0,0,0,0,5,5,5,5,5,5,10,10,10,10,10,10,10,20]
threshold=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

#temporary variables
values=[]
values_index=[]

year_max=0
year_min=3000
runtime_max=0
runtime_min=1000

#output variables
info_output=[]
rating_output=[]


def connect_to_sql():
    global cur,conn
    try:
        conn = MySQLdb.connect(mysql_ip, mysql_user, mysql_passwd, mysql_db, charset='utf8')
        cur = conn.cursor()
        print ' - CONNECT_TO_SQL - Connect successfully.'
    except Exception as e:
        print ' - CONNECT_TO_SQL - An {} exception occured.'.format(e)

def scan_column():
    global cur,conn
    global year_max,year_min,runtime_max,runtime_min
    try:
        index=0
        for keyword in info_cols:
            values_index.append(index)
            cur.execute('SELECT %s FROM new_movies' % keyword)
            result=cur.fetchall()

            if keyword=='year' or keyword=='runtimes':
                for instance in result:
                    instance=int(instance[0])
                    if keyword=='year':
                        if instance>year_max:
                            year_max=instance
                        elif instance<year_min:
                            year_min=instance
                    else:
                        if instance>runtime_max:
                            runtime_max=instance
                        elif instance<runtime_min:
                            runtime_min=instance
                values.append(keyword)
                index+=1
            else:
                temp_values_counter=[]
                temp_values=[]
                for instance in result:
                    for i in instance[0].split('$'):
                        if temp_values.count(i)==0:
                            temp_values.append(i)
                            temp_values_counter.append(1)
                        else:
                            temp_values_counter[temp_values.index(i)]+=1
                for i in xrange(0,len(temp_values_counter)):
                    if temp_values_counter[i]>threshold[info_cols.index(keyword)]:
                        values.append(temp_values[i])
                        index+=1
                values.append('others_%s' % keyword)
                index+=1        
            conn.commit()
            print ' - SCAN_COLUMN - Keyword: %s Scan successfully.' % keyword
        values_index.append(index)
    except Exception as e:
            print ' - SCAN_COLUMN - An {} exception occured'.format(e)

def generate_table():
    global cur,conn
    global year_max,year_min,runtime_max,runtime_min
    printvars()
    try:
        cur.execute('SELECT id FROM new_movies')
        id_result=cur.fetchall()
        conn.commit()
        for movie_id in id_result:
            movie_info=[]
            movie_rating=[]
            rating_sum=0.0
            print ' - SCAN_ROW - ID: %s Scanning.' % movie_id[0]
            for keyword in info_cols:
                cur.execute("SELECT %s FROM new_movies WHERE id= '%s'" % (keyword,str(movie_id[0])))
                result = cur.fetchall()
                if keyword=="year":
                    var=(float(result[0][0])-year_min)/(year_max-year_min)
                    movie_info.append(var)
                elif keyword=="runtimes":
                    var=(float(result[0][0])-runtime_min)/(runtime_max-runtime_min)
                    movie_info.append(var)
                else:
                    flag=0.0
                    #TODO question?
                    for i in xrange(values_index[info_cols.index(keyword)],values_index[info_cols.index(keyword)+1]-1):
                        if result[0][0] == '': 
                            movie_info.append(0.0)
                        else:
                            r=0.0
                            for value in result[0][0].split('$'): 
                                if values[i] == value:
                                    r=1.0
                                else:
                                    flag=1.0
                            movie_info.append(r)
                    movie_info.append(flag)   
                conn.commit()
            print len(movie_info)
            for keyword in rating_cols:
                cur.execute("SELECT %s FROM new_movies WHERE id= '%s'" % (keyword,str(movie_id[0])))
                result = cur.fetchall()
                rating_sum=rating_sum+float(result[0][0])
                movie_rating.append(float(result[0][0]))
                conn.commit()
            for i in xrange(0,len(movie_rating)):
                movie_rating[i]=movie_rating[i]/rating_sum
            print ' - SCAN_ROW - ID: %s Scan successfully.' % movie_id[0]
    except Exception as e:
            print ' - GENERATE_TABLE - An {} exception occured'.format(e)
    movie=[]


def printvars():
    print len(values)
    print values
    print values_index
    #print str(year_max)+' '+str(year_min)
    #print str(runtime_max) +' ' + str(runtime_min)

if __name__ == '__main__':
    connect_to_sql()
    scan_column()
    generate_table()
    conn.close()
    print 'Done crawling data from IMDB!'


