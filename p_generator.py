import sqlite3
import numpy as np
import bfgslld as alg
import predict


lFtrCols = ["year", "runtimes", "genres", 'color_info', 'director', 'cast_1st',
               'cast_2nd', 'cast_3rd', 'countries', 'languages', 'writer',
               'editor', 'cinematographer', 'art_director', 'costume_designer',
               'original_music', 'sound_mix', 'production_companies']
lRtgCols = ["real_1", "real_2", "real_3", "real_4", "real_5", "real_6",
               "real_7", "real_8", "real_9", "real_10"]
lRnk = ['Top5','Top50','Top500','Top5000','5000+']

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
            print "-GENERATE- Scanning %s..." % ctlg
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
                if ctlg in ['cast_1st','cast_2nd', 'cast_3rd']:
                    for r in lRnk:
                        lValue.append(r+'_'+ctlg)
                    index += len(lRnk)
                else:
                    lValue.append('Others_%s' % ctlg)
                    index += 1        
                if nullflag:
                    lValue.append('Null_%s' % ctlg)
                    index += 1
            conn.commit()
            # print '-SCAN- Catalog %s scan successfully.' % ctlg
        idxCtlg.append(index)
    except Exception as e:
            print '-SCAN- An {} exception occured'.format(e)
    return (idxCtlg,lValue)


def generate_matrices(mvID,cur,conn,idxCtlg,lValue):
    global mxYear, mnYear, mxRntms, mnRntms
    try:
        oneFtr = np.zeros((1, len(lValue)), dtype=np.double)
        oneLbl = np.zeros((1, 10), dtype=np.double)
        for ctlg in lFtrCols:
            cur.execute("SELECT %s FROM feature WHERE id= '%s'" % (ctlg, str(mvID)))
            rst = cur.fetchall()
            for i in xrange(idxCtlg[lFtrCols.index(ctlg)], idxCtlg[lFtrCols.index(ctlg)+1]):
                if ctlg in ["year", "runtimes"]:
                    if int(rst[0][0]) == 0:
                        oneFtr[0, i] = 0.0
                        oneFtr[0, idxCtlg[lFtrCols.index(ctlg)+1] - 1] = 1.0
                    else:
                        if ((idxCtlg[lFtrCols.index(ctlg)+1] - 1) == i) and (idxCtlg[lFtrCols.index(ctlg)+1] - 1 - idxCtlg[lFtrCols.index(ctlg)]) > 0:
                            continue
                        if ctlg == "year":
                            var = (float(rst[0][0]) - mnYear) / (mxYear - mnYear)
                        else:
                            var = (float(rst[0][0]) - mnRntms) / (mxRntms - mnRntms)
                        oneFtr[0, i] = var
                else:
                    otrs = False
                    # inc = 1.0/(idxCtlg[lFtrCols.index(ctlg)+1] - idxCtlg[lFtrCols.index(ctlg)] - 1)
                    if rst[0][0] == '':
                        # null column equals 1
                        oneFtr[0, idxCtlg[lFtrCols.index(ctlg) + 1] - 1] = 1.0
                        continue
                    else:
                        r=0.0
                        for value in rst[0][0].split('$'): 
                            if lValue[i] == value:
                                r = 1.0
                            else:
                                # otrs += inc
                                otrs = True
                        oneFtr[0, i] = r
                    if otrs:
                        if ctlg in ['cast_1st','cast_2nd', 'cast_3rd']:
                            cur.execute("SELECT %s FROM feature WHERE id= '%s'" % (ctlg+('_rank'), str(mvID)))
                            rank = cur.fetchone() 
                            offset = 6 - lRnk.index(rank[0])
                            oneFtr[0, idxCtlg[lFtrCols.index(ctlg) + 1]-offset]=1.0
                        else:
                            # others column equals 1
                            oneFtr[0, idxCtlg[lFtrCols.index(ctlg) + 1] - 1] = 1.0  
            conn.commit()
        for keyword in lRtgCols:
            cur.execute("SELECT %s FROM rating WHERE id= '%s'" % (keyword, str(mvID)))
            rst = cur.fetchall()
            oneLbl[0, lRtgCols.index(keyword)] = float(rst[0][0])
        # print ' - SCAN_ROW - ID: %s Scan successfully.' % mvID    
    except Exception as e:
        print '-GENERATE_MATRICES- An {} exception occured!'.format(e)
    return (oneFtr, oneLbl)