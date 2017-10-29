import sqlite3
import scipy.io as sio
import numpy as np


mode = "old"

cur = None
conn = None

lFtrCols = ["year", "runtimes", "genres", 'color_info', 'director', 'cast_1st',
               'cast_2nd', 'cast_3rd', 'countries', 'languages', 'writer',
               'editor', 'cinematographer', 'art_director', 'costume_designer',
               'original_music', 'sound_mix', 'production_companies']
lRtgCols = ["real_1", "real_2", "real_3", "real_4", "real_5", "real_6",
               "real_7", "real_8", "real_9", "real_10"]

# threshold = [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 7]
threshold = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

# temporary variables
lValue = []
idxCtlg = []

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
            idxCtlg.append(index)
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
                # check whether numbers of value is greater 
                # than the threshold of this catalog
                for key in tmpDictValue:
                    if tmpDictValue[key] > threshold[lFtrCols.index(ctlg)]:
                        # add the value in  column list
                        lValue.append(key)
                        index += 1
                if nullflag:
                    lValue.append('Null_%s' % ctlg)
                    index += 1
                lValue.append('Others_%s' % ctlg)
                index += 1
            conn.commit()
            print '-SCAN- Catalog %s scan successfully.' % ctlg
        idxCtlg.append(index)
    except Exception as e:
            print '-SCAN- An {} exception occured'.format(e)


def generate_matrices():
    global cur, conn
    global mxYear, mnYear, mxRntms, mnRntms
    global info_output, rating_output, mode
    # printvars()
    try:
        cur.execute('SELECT id FROM feature')
        rstID = cur.fetchall()
        conn.commit()
        info_output = np.zeros((len(rstID), len(lValue)), dtype=np.double)
        rating_output = np.zeros((len(rstID), 10), dtype=np.double)
        for mvID in rstID:
            idxRow = rstID.index(mvID)
            for ctlg in lFtrCols:
                cur.execute("SELECT %s FROM feature WHERE id= '%s'" % (ctlg, str(mvID[0])))
                rst = cur.fetchall()
                for i in xrange(idxCtlg[lFtrCols.index(ctlg)], idxCtlg[lFtrCols.index(ctlg)+1]):
                    if ctlg == "year" or ctlg == "runtimes":
                        if int(rst[0][0]) == 0:
                            info_output[idxRow, i] = 0.0
                            info_output[idxRow, idxCtlg[lFtrCols.index(ctlg)+1] - 1] = 1.0
                        else:
                            if ((idxCtlg[lFtrCols.index(ctlg)+1] - 1) == i) and (idxCtlg[lFtrCols.index(ctlg)+1] - 1 - idxCtlg[lFtrCols.index(ctlg)]) > 0:
                                continue
                            if ctlg == "year":
                                var = (float(rst[0][0]) - mnYear) / (mxYear - mnYear)
                            else:
                                var = (float(rst[0][0]) - mnRntms) / (mxRntms - mnRntms)
                            info_output[idxRow, i] = var
                    else:
                        otrs = 0.0
                        inc = 1.0/(idxCtlg[lFtrCols.index(ctlg)+1] - idxCtlg[lFtrCols.index(ctlg)] - 1)
                        if rst[0][0] == '':
                            # null column equals 1
                            info_output[idxRow, idxCtlg[lFtrCols.index(ctlg) + 1] - 2] = 1.0
                            continue
                        else:
                            r=0.0
                            for value in rst[0][0].split('$'): 
                                if lValue[i] == value:
                                    r = 1.0
                                else:
                                    otrs += inc
                            info_output[idxRow, i] = r
                        # others column equals 1
                        info_output[idxRow, idxCtlg[lFtrCols.index(ctlg) + 1] - 1] = otrs  
                conn.commit()
            if mode == "old":
                for keyword in lRtgCols:
                    cur.execute("SELECT %s FROM rating WHERE id= '%s'" % (keyword, str(mvID[0])))
                    rst = cur.fetchall()
                    rating_output[idxRow, lRtgCols.index(keyword)] = float(rst[0][0])
            print ' - SCAN_ROW - ID: %s Scan successfully.' % mvID[0]
            idxRow += 1
    except Exception as e:
            print ' - GENERATE_MATRICES - An {} exception occured'.format(e)


def printvars():
    global mxYear, mnYear, mxRntms, mnRntms
    print len(lValue)
    # print lValue
    print idxCtlg
    # print str(mxYear) + ' '+str(mnYear)
    # print str(mxRntms) + ' ' + str(mnRntms)


if __name__ == '__main__':
    connect_to_sql()
    scan_column()
    printvars()
    generate_matrices()
    if mode == "old":
        np.savetxt('info.txt', info_output)
        np.savetxt('rating.txt', rating_output)
    # elif mode == "new":
    #     np.savetxt('f_info.txt', info_output)
    conn.close()
    print 'Done generating matrices from database!'


