import pymysql
import logging
import numpy as np
import bfgslld as alg
import generator
import functions


# temporary variables
lValue = []
idxCtlg = []

cur = None
conn = None

def connect_to_sql():
    global cur, conn
    try:
        conn = pymysql.connect(host='movie-data.ch6y02vfazod.ap-northeast-1.rds.amazonaws.com',
                             user='admin',
                             password='*******',
                             database='movierating',
                             port=3306,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        logging.info('-PREDICTION- Connect to database successfully.')
    except Exception as e:
        logging.exception('-- An {} exception occured.'.format(e))


def predict(slctMvID,prefix):
    global oTrnFtr,oTrnLbl,oTstFtr
    logging.info("-ALGORITHM- Training model...")
    oPdctLbl=alg.run(oTrnFtr,oTrnLbl,oTstFtr)
    logging.info("-PREDICTION- Recording results...")
    sql="UPDATE `data` SET `predict_1`=%f, `predict_2`=%f, `predict_3`=%f, `predict_4`=%f, `predict_5`=%f, `predict_6`=%f, `predict_7`=%f, `predict_8`=%f, `predict_9`=%f, `predict_10`=%f WHERE id = %s;"
    for i in range(oPdctLbl.shape[0]):
        cur.execute(sql % (oPdctLbl[i][0],oPdctLbl[i][1],oPdctLbl[i][2],oPdctLbl[i][3],oPdctLbl[i][4],oPdctLbl[i][5],oPdctLbl[i][6],oPdctLbl[i][7],oPdctLbl[i][8],oPdctLbl[i][9],slctMvID[i]))
        cur.execute('UPDATE `data` SET `for` = "show" WHERE `id` = %s;',(slctMvID[i],))
    conn.commit()

def cal_metric(prefix,slctMvID):
    real=[]
    predict=[]
    for mvID in slctMvID:
        cur.execute('SELECT `real_1`,`real_2`,`real_3`,`real_4`,`real_5`,`real_6`,`real_7`,`real_8`,`real_9`,`real_10` FROM `data` WHERE `id` = %s;',(mvID,))
        rstID = cur.fetchone()
        real=list(rstID.values())
        cur.execute('SELECT `predict_1`, `predict_2`, `predict_3`, `predict_4`, `predict_5`, `predict_6`, `predict_7`, `predict_8`, `predict_9`, `predict_10` FROM `data` WHERE `id` = %s;'
        ,(mvID,))
        rstID = cur.fetchone()
        predict=list(rstID.values())
        m=functions.k_l(predict,real)
        cur.execute('UPDATE `data` SET `metric` = %s WHERE `id` = %s;',(m,mvID))
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
    cur.execute('SELECT `id` FROM `data` WHERE `for` = "train";')
    rstID = cur.fetchall()
    for mvID in rstID:
        (oneFtr, oneLbl) = generator.generate_matrices(mvID['id'],cur,conn,idxCtlg,lValue)
        if oTrnFtr is None:
            oTrnFtr = oneFtr
            oTrnLbl = oneLbl
        else:
            oTrnFtr = np.concatenate((oTrnFtr, oneFtr))
            oTrnLbl = np.concatenate((oTrnLbl, oneLbl))


    logging.info('-GENERATE_DATASET- Finished on generating train set.')

    # generate test set 
    cur.execute('SELECT `id` FROM `data` WHERE `for` = "test";')
    rstID = cur.fetchall()
    for mvID in rstID:
        slctMvID.append(mvID['id'])
        (oneFtr, oneLbl) = generator.generate_matrices(mvID['id'],cur,conn,idxCtlg,lValue)
        if oTstFtr is None:
            oTstFtr = oneFtr
            oTstLbl = oneLbl
        else:
            oTstFtr = np.concatenate((oTstFtr, oneFtr))
            oTstLbl = np.concatenate((oTstLbl, oneLbl))   

    logging.info('-GENERATE_DATASET- Finished on generating test set.')        
    # train the model
    predict(slctMvID,prefix)
    # calculate k-l distance
    cal_metric(prefix,slctMvID)


def run():
    global idxCtlg,lValue
    connect_to_sql()
    (idxCtlg,lValue)=generator.scan_column(cur,conn)
    convert()
    conn.close()
