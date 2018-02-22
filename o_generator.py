import sqlite3
import numpy as np


lFtrCols = ["year", "runtimes","genres", 'color_info', 'cast_1st','cast_2nd', 'cast_3rd', 
                'countries', 'languages', 'director' ,'writer',"producer",
               'composers', 'cinematographer', 'editor', 'art_director', 
               'costume_designer', 'production_companies']
lRtgCols = ["real_1", "real_2", "real_3", "real_4", "real_5", "real_6",
               "real_7", "real_8", "real_9", "real_10"]

# threshold = [0, 0, 0, 0, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 7]
threshold = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

mxYear = 0
mnYear = 3000
mxRntms = 0
mnRntms = 1000



def scan_column(cur,conn):
    global mxYear, mnYear, mxRntms, mnRntms
    idxCtlg =[]
    lValue=[]
    try:
        index = 0
        for ctlg in lFtrCols:
            idxCtlg.append(index)
            command = "SELECT %s FROM feature" % ctlg
            #  print "executing %s..." % command
            cur.execute(command)
            print ("-GENERATE- Scanning %s..." % ctlg)
            result = cur.fetchall()
            # get the max& min value of year and runtimes by iteration
            if ctlg in ['year','runtimes']:
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
                    lValue.append("NULL_" + ctlg)
                    index += 1
            else:
                # a dict to count number of each value
                tmpDictValue = {}
                # whether has null string in this catalog
                nullflag = False
                for instance in result:
                    if instance[0] == 'NULL':
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
                    lValue.append('NULL_%s' % ctlg)
                    index += 1
                if threshold[lFtrCols.index(ctlg)] == 0:
                    continue
                lValue.append('Others_%s' % ctlg)
                index += 1
            conn.commit()
            # print '-SCAN- Catalog %s scan successfully.' % ctlg
        idxCtlg.append(index)
    except Exception as e:
            print ('-SCAN- An {} exception occured'.format(e))
    return (idxCtlg,lValue)

def generate_matrices(mvID,cur,conn,idxCtlg,lValue):
    global mxYear, mnYear, mxRntms, mnRntms
    try:
        oneFtr = np.zeros((1, len(lValue)), dtype=np.double)
        oneLbl = np.zeros((1, 10), dtype=np.double)
        for ctlg in lFtrCols:
            cur.execute("SELECT %s FROM feature WHERE id= '%s'" % (ctlg, str(mvID)))
            rst = cur.fetchone()
            if ctlg == "year" or ctlg == "runtimes":
                if int(rst[0]) == 0: # NULL
                    oneFtr[0, i] = 0.0
                    oneFtr[0, idxCtlg[lFtrCols.index(ctlg)+1] - 1] = 1.0
                else:
                    if ctlg == "year":
                        var = (float(rst[0]) - mnYear) / (mxYear - mnYear)
                    else:
                        var = (float(rst[0]) - mnRntms) / (mxRntms - mnRntms)
                    oneFtr[0, idxCtlg[lFtrCols.index(ctlg)]] = var
            else:
                if rst[0] == 'NULL':
                    # null column equals 1
                    if threshold[lFtrCols.index(ctlg)] == 0: #has no others column
                        oneFtr[0, idxCtlg[lFtrCols.index(ctlg) + 1] - 1] = 1.0
                    else:
                        oneFtr[0, idxCtlg[lFtrCols.index(ctlg) + 1] - 2] = 1.0
                    continue
                else:
                    counter = 0
                    for value in rst[0].split('$'):
                        for i in range(idxCtlg[lFtrCols.index(ctlg)], idxCtlg[lFtrCols.index(ctlg)+1]):
                            if lValue[i] == value:
                                oneFtr[0, i]=1.0
                                counter += 1
                                break
                    if len(rst[0].split('$'))>counter: # others = 1.0
                        oneFtr[0, idxCtlg[lFtrCols.index(ctlg) + 1] - 1]=1.0
            conn.commit()
        for keyword in lRtgCols:
            cur.execute("SELECT %s FROM rating WHERE id= '%s'" % (keyword, str(mvID)))
            rst = cur.fetchone()
            oneLbl[0, lRtgCols.index(keyword)] = float(rst[0])
        # print ' - SCAN_ROW - ID: %s Scan successfully.' % mvID
    except Exception as e:
        print ('-GENERATE_MATRICES- An {} exception occured!'.format(e))
    return (oneFtr, oneLbl)