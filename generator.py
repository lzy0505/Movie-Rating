import sqlite3
import numpy as np


mode = "old"

cur = None
conn = None

lFtrCols = ["year", "runtimes", "genres", 'color_info', 'director', 'cast_1st', 'cast_2nd', 'cast_3rd', 'countries', 'languages',
    'writer', 'editor', 'cinematographer', 'art_director', 'costume_designer', 'original_music', 'sound_mix', 'production_companies']
lRtgCols = []

#threshold = [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 7]
threshold=[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

# temporary variables
lValue = []
idxValue = []

mxYear = 0
mnYear = 3000
mxRntms = 0
mnRntms = 1000

# output variables
info_output = None
rating_output = None


def connect_to_sql():
    global cur, conn
    try:
        conn = sqlite3.connect('movie.db')
        cur = conn.cursor()
        print '-GENERATE- Connect to database successfully.'
    except Exception as e:
        print '-- An {} exception occured.'.format(e)


def scan_column():
    global cur, conn
    global mxYear, mnYear, mxRntms, mnRntms
    try:
        index = 0
        for ctlg in lFtrCols:
            idxValue.append(index)
            command = "SELECT %s FROM feature" % ctlg
            print "executing %s..." % command
            cur.execute(command)
            print "scanning %s..." % ctlg
            result = cur.fetchall()
            # get the max& min value of year and runtimes by iteration
            if ctlg == 'year' or ctlg == 'runtimes':
                nullflag = False
                for instance in result:
                    if instance[0] == 0:
                        nullflag = True
                        continue
                    instance = int(instance[0])
                    if ctlg == 'year':
                        if instance > mxYear:
                            mxYear = instance
                        elif instance < mnYear:
                            mnYear = instance
                    else:
                        if instance > mxRntms:
                            mxRntms = instance
                        elif instance < mnRntms:
                            mnRntms = instance
                lValue.append(ctlg)
                index += 1
                if nullflag:
                    lValue.append("Null_" + ctlg)
                    index += 1
            else:
                # a dict to count number of each value
                tmpDictValue = {}
                # whether has null string in this catalog
                nullflag = False
                for instance in result:
                    if instance[0] == '':
                        nullflag = True
                    for i in instance[0].split('$'):
                        # if no such key in dict
                        if i not in tmpDictValue.keys():
                            tmpDictValue[i] = 1
                        else:
                            tmpDictValue[i] += 1
                # check whether numbers of value is greater than the threshold of this catalog
                for key in tmpDictValue:
                    if tmpDictValue[key] > threshold[lFtrCols.index(ctlg)]:
                        # add the value in  column list
                        lValue.append(key)
                        index += 1
                if nullflag:
                    lValue.append('Null_%s' % ctlg)
                    index += 1
                lValue.append('others_%s' % ctlg)
                index += 1
            conn.commit()
            print '-SCAN- Catalog %s scan successfully.' % ctlg
        idxValue.append(index)
    except Exception as e:
            print '-SCAN- An {} exception occured'.format(e)


# def generate_matrices():
#     global cur,conn
#     global year_max,year_min,runtime_max,runtime_min
#     global info_output,rating_output
#     #printvars()
#     try:
#         cur.execute('SELECT id FROM %s' % mysql_table)
#         id_result=cur.fetchall()
#         conn.commit()
#         info_output=np.zeros((len(id_result), len(values)), dtype=np.double)
#         rating_output=np.zeros((len(id_result), 10), dtype=np.double)
#         row_index=0
#         for movie_id in id_result:
#             movie_rating=[]
#             rating_sum=0.0
#             for keyword in info_cols:
#                 cur.execute("SELECT %s FROM %s WHERE id= '%s'" % (keyword,mysql_table,str(movie_id[0])))
#                 result = cur.fetchall()
#                 if keyword=="year":
#                     var=(float(result[0][0])-year_min)/(year_max-year_min)
#                     info_output[row_index,0]=var
#                 elif keyword=="runtimes":
#                     var=(float(result[0][0])-runtime_min)/(runtime_max-runtime_min)
#                     info_output[row_index,1]=var
#                 else:
#                     flag=0.0
#                     for i in xrange(values_index[info_cols.index(keyword)],values_index[info_cols.index(keyword)+1]-1):
#                         if result[0][0] == '': 
#                             info_output[row_index,i]=0.0
#                             info_output[row_index,values_index[info_cols.index(keyword)+1]-2]=1.0
#                         else:
#                             r=0.0
#                             for value in result[0][0].split('$'): 
#                                 if values[i] == value:
#                                     r=1.0
#                                 else:
#                                     flag=1.0
#                             info_output[row_index,i]=r
#                     info_output[row_index,values_index[info_cols.index(keyword)+1]-1]=flag  
#                 conn.commit()
#             if mysql_table=='new_movies':
#                 for keyword in rating_cols:
#                     cur.execute("SELECT %s FROM new_movies WHERE id= '%s'" % (keyword,str(movie_id[0])))
#                     result = cur.fetchall()
#                     rating_sum=rating_sum+float(result[0][0])
#                     movie_rating.append(float(result[0][0]))
#                     conn.commit()
#                 for i in xrange(0,len(movie_rating)):
#                     rating_output[row_index,i]=movie_rating[i]/rating_sum
                
#             print ' - SCAN_ROW - ID: %s Scan successfully.' % movie_id[0]
#             row_index+=1
#     except Exception as e:
#             print ' - GENERATE_MATRICES - An {} exception occured'.format(e)


def printvars():
    global mxYear, mnYear, mxRntms, mnRntms
    print len(lValue)
    print lValue
    print idxValue
    print str(mxYear) + ' '+str(mnYear)
    print str(mxRntms) + ' ' + str(mnRntms)


if __name__ == '__main__':
    connect_to_sql()
    scan_column()
    printvars()
    # generate_matrices()
    # if mode == "old":
    #     np.savetxt('info.txt', info_output)
    #     np.savetxt('rating.txt', rating_output)
    # elif mode == "new":
    #     np.savetxt('f_info.txt', info_output)
    conn.close()
    print 'Done generating matrices from database!'


