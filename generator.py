import sqlite3
import scipy.io as sio
import numpy as np
import random


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


def generate_matrices(mvID):
    global cur, conn
    global mxYear, mnYear, mxRntms, mnRntms
    global mode
    try:
        oneFtr = np.zeros((1, len(lValue)), dtype=np.double)
        oneLbl = np.zeros((1, 10), dtype=np.double)
        for ctlg in lFtrCols:
            cur.execute("SELECT %s FROM feature WHERE id= '%s'" % (ctlg, str(mvID)))
            rst = cur.fetchall()
            for i in xrange(idxCtlg[lFtrCols.index(ctlg)], idxCtlg[lFtrCols.index(ctlg)+1]):
                if ctlg == "year" or ctlg == "runtimes":
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
                    otrs = 0.0
                    inc = 1.0/(idxCtlg[lFtrCols.index(ctlg)+1] - idxCtlg[lFtrCols.index(ctlg)] - 1)
                    if rst[0][0] == '':
                        # null column equals 1
                        oneFtr[0, idxCtlg[lFtrCols.index(ctlg) + 1] - 2] = 1.0
                        continue
                    else:
                        r=0.0
                        for value in rst[0][0].split('$'): 
                            if lValue[i] == value:
                                r = 1.0
                            else:
                                otrs += inc
                        oneFtr[0, i] = r
                    # others column equals 1
                    oneFtr[0, idxCtlg[lFtrCols.index(ctlg) + 1] - 1] = otrs  
            conn.commit()
        if mode == "old":
            for keyword in lRtgCols:
                cur.execute("SELECT %s FROM rating WHERE id= '%s'" % (keyword, str(mvID)))
                rst = cur.fetchall()
                oneLbl[0, lRtgCols.index(keyword)] = float(rst[0][0])
        print ' - SCAN_ROW - ID: %s Scan successfully.' % mvID
        return (oneFtr, oneLbl)
    except Exception as e:
        print ' - GENERATE_MATRICES - An {} exception occured'.format(e)


def convert():
    if mode == "new":
        # train set & test set
        oTrnFtr = None
        oTrnLbl = None
        oTstFtr = None

        cur.execute('SELECT id FROM feature WHERE mode = "old"')
        rstID = cur.fetchall()
        for mvID in rstID:
            (oneFtr, oneLbl) = generate_matrices(mvID[0])
            if oTrnFtr is None:
                oTrnFtr = oneFtr
                oTrnLbl = oneLbl
            else:
                oTrnFtr = np.concatenate((oTrnFtr, oneFtr))
                oTrnLbl = np.concatenate((oTrnLbl, oneLbl))

        cur.execute('SELECT id FROM feature WHERE mode = "new"')
        rstID = cur.fetchall()
        for mvID in rstID:
            (oneFtr, oneLbl) = generate_matrices(mvID[0])
            if oTstFtr is None:
                oTstFtr = oneFtr
            else:
                oTstFtr = np.concatenate((oTrnFtr, oneFtr))

        (r, c) = oTrnFtr.shape
        trainNum = r
        (r, c) = oTstFtr.shape
        testNum = r

        print oTrnFtr.shape
        print oTrnLbl.shape
        print oTstFtr.shape

        sio.savemat('f_movieDataSet.mat', {'testFeature':oTstFtr, 'testNum':testNum, 'trainDistribution':oTrnLbl, 'trainFeature':oTrnFtr, 'trainNum':trainNum})
    elif mode == "old":

        cur.execute('SELECT id FROM feature WHERE mode = "old"')
        rstID = cur.fetchall()

        # record the mvid of selected instance
        slctMvID = []
        # randomly select 1/numPrtn of instances
        numPrtn = 10

        # train set & test set
        oTrnFtr = None
        oTrnLbl = None
        oTstFtr = None
        oTstLbl = None 

        # generate random number
        for i in xrange(0, int(len(rstID)/numPrtn)):
            r = random.randint(0, len(rstID))
            while rstID[r][0] in slctMvID:
                r = random.randint(0, len(rstID))
            slctMvID.append(rstID[r][0])
        
        # generate train set & test set
        for mvID in rstID:
            (oneFtr, oneLbl) = generate_matrices(mvID[0])
            if mvID[0] in slctMvID:   
                if oTstFtr is None:
                    oTstFtr = oneFtr
                    oTstLbl = oneLbl
                else:
                    oTstFtr = np.concatenate((oTstFtr, oneFtr))
                    oTstLbl = np.concatenate((oTstLbl, oneLbl))
            else:
                if oTrnFtr is None:
                    oTrnFtr = oneFtr
                    oTrnLbl = oneLbl
                else:
                    oTrnFtr = np.concatenate((oTrnFtr, oneFtr))
                    oTrnLbl = np.concatenate((oTrnLbl, oneLbl))
        
        # get size of train set & test set
        (r, c) = oTrnFtr.shape
        trainNum = r
        (r, c) = oTstFtr.shape
        testNum = r

        print oTrnFtr.shape
        print oTrnLbl.shape
        print oTstFtr.shape
        print oTstLbl.shape
        print trainNum + testNum

    sio.savemat('o_movieDataSet.mat', {'testDistribution': oTstLbl, 'testFeature': oTstFtr, 'testNum':testNum,'trainDistribution':oTrnLbl,'trainFeature':oTrnFtr,'trainNum':trainNum})


def printvars():
    global mxYear, mnYear, mxRntms, mnRntms
    print len(lValue)
    # print lValue
    print idxCtlg


if __name__ == '__main__':
    connect_to_sql()
    scan_column()
    printvars()
    convert()
    conn.close()
    print 'Done generating matrices from database!'