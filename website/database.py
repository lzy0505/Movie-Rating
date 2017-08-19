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


test_index=[]
test_result=[]




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




if __name__ == '__main__':
    get_instance_basic('new_movies')



