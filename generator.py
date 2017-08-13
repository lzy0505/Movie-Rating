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


#temporary variables
values=[]
keywords_index=[]

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
            keywords_index.append(index)
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
                index=index+1
            else:
                for instance in result:
                    for i in instance[0].split('$'):
                        if values.count(i)==0:
                            values.append(i)
                            index=index+1
            
            conn.commit()
            print ' - SCAN_COLUMN - Keyword: %s Scan successfully.' % keyword

    except Exception as e:
            print ' - SCAN_COLUMN - An {} exception occured'.format(e)

def generate_table():
    #TODO
    printvars()
    movie=[]

def printvars():
    print values
    print keywords_index
    print str(year_max)+' '+str(year_min)
    print str(runtime_max) +' ' + str(runtime_min)

if __name__ == '__main__':
    connect_to_sql()
    scan_column()
    generate_table()
    conn.close()
    print 'Done crawling data from IMDB!'


