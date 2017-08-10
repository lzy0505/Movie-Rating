import MySQLdb
from movie import Movie

mysql_ip = 'localhost'
mysql_user = 'root'
mysql_passwd = 'root'
mysql_db = 'mv'

output=[]

string_cols=['genres','color_info','director','cast_1','cast_2','cast_3','countries','languages',
'writer','editor','cinematographer','art_direction','costume_designer','original_music','sound_mix',
'production_companies']
int_cols=['year','runtimes','number_of_votes_1','number_of_votes_2','number_of_votes_3',
'number_of_votes_4','number_of_votes_5','number_of_votes_6','number_of_votes_7','number_of_votes_8',
'number_of_votes_9','number_of_votes_10']

values=[]
keywords_index=[]
cur=None
conn=None

def connect_to_sql():
    global cur,conn
    try:
        conn = MySQLdb.connect(mysql_ip, mysql_user, mysql_passwd, mysql_db, charset='utf8')
        cur = conn.cursor()
        print ' - CONNECT_TO_SQL - Connect successfully.'
    except Exception as e:
        print ' - CONNECT_TO_SQL - An {} exception occured.'.format(e)

def scan_values():
    global cur,conn
    try:
        index=0
        for keyword in string_cols:
            keywords_index.append(index)
            cur.execute('SELECT %s FROM new_movies' % keyword)
            result=cur.fetchall()
            for instance in result:
                for i in instance[0].split('$'):
                    if values.count(i)==0:
                        values.append(i)
                        index=index+1
            conn.commit()
            print ' - SCAN_VALUES - Keyword: %s scan successfully.' % keyword
        
        #print values
        #print keywords_index
    except Exception as e:
            print ' - SCAN_VALUES - An {} exception occured'.format(e)

def generate_table():
    #TODO
    movie=[]

if __name__ == '__main__':
    connect_to_sql()
    scan_values()
    generate_table()
    conn.close()
    print 'Done crawling data from IMDB!'


