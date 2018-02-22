import sqlite3
import numpy as np
import bfgslld as alg
# import p_generator
import o_generator

lPtgCols = ["predict_1", "predict_2", "predict_3", "predict_4", "predict_5", "predict_6",
"predict_7", "predict_8", "predict_9", "predict_10"]

# temporary variables
lValue = []
idxCtlg = []

cur = None
conn = None

def connect_to_sql():
    global cur, conn
    try:
        conn = sqlite3.connect('movie.db')
        cur = conn.cursor()
        print ('-PREDICTION- Connect to database successfully.')
    except Exception as e:
        print ('-- An {} exception occured.'.format(e))


def predict(slctMvID,prefix):
    global oTrnFtr,oTrnLbl,oTstFtr
    print ("-ALGORITHM- Training model...")
    oPdctLbl=alg.run(oTrnFtr,oTrnLbl,oTstFtr)
    print ("-PREDICTION- Recording results...")
    for i in range(oPdctLbl.shape[0]):
        for j in range(oPdctLbl.shape[1]):
            cur.execute('UPDATE rating SET %s = ? WHERE id = ?'%(prefix+lPtgCols[j]),(oPdctLbl[i][j],slctMvID[i]))
        cur.execute('UPDATE feature SET for = "test" WHERE id = %s'%(slctMvID[i]))
    conn.commit()

def convert(prefix):
    global oTrnFtr,oTrnLbl,oTstFtr
    # record the mvid of selected instance
    slctMvID = []

    # train set & test set
    oTrnFtr = None
    oTrnLbl = None
    oTstFtr = None
    oTstLbl = None
    
    # generate train set 
    cur.execute('SELECT id FROM feature WHERE for = "train"')
    rstID = cur.fetchall()
    for mvID in rstID:
        if prefix is 'o_':
            (oneFtr, oneLbl) = o_generator.generate_matrices(mvID[0],cur,conn,idxCtlg,lValue)
        # elif prefix is 'p_':
            # (oneFtr, oneLbl) = p_generator.generate_matrices(mvID[0],cur,conn,idxCtlg,lValue)
        if oTrnFtr is None:
            oTrnFtr = oneFtr
            oTrnLbl = oneLbl
        else:
            oTrnFtr = np.concatenate((oTrnFtr, oneFtr))
            oTrnLbl = np.concatenate((oTrnLbl, oneLbl))
            
    # generate test set 
    cur.execute('SELECT id FROM feature WHERE for = "test"')
    rstID = cur.fetchall()
    for mvID in rstID:
        slctMvID.append(mvID[0])
        if prefix is 'o_':
            (oneFtr, oneLbl) = o_generator.generate_matrices(mvID[0],cur,conn,idxCtlg,lValue)
        # else prefix is 'p_':
        #     (oneFtr, oneLbl) = o_generator.generate_matrices(mvID[0],cur,conn,idxCtlg,lValue)
        if oTstFtr is None:
            oTstFtr = oneFtr
            oTstLbl = oneLbl
        else:
            oTstFtr = np.concatenate((oTstFtr, oneFtr))
            oTstLbl = np.concatenate((oTstLbl, oneLbl))        
            
    # train the model
    predict(slctMvID,prefix)


# def printvars():
#     global oTrnFtr,oTrnLbl,oTstFtr
#     print len(lValue)
#     print idxCtlg
#     print oTrnFtr.shape
#     print oTrnLbl.shape
#     print oTstFtr.shape

def run():
    global idxCtlg,lValue
    connect_to_sql()
    (idxCtlg,lValue)=o_generator.scan_column(cur,conn)
    convert('o_')#old dataset
    # (idxCtlg,lValue)=p_generator.scan_column(cur,conn)
    # convert('p_')#new dataset

if __name__ == '__main__':
    run()