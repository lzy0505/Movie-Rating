import pymysql
import numpy as np
import bfgslld as alg
# import p_generator
import o_generator
import functions
import time


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
                             password='123',
                             database='movierating',
                             port=3306,
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
        cur = conn.cursor()
        print ('-PREDICTION- Connect to database successfully.')
    except Exception as e:
        print ('-- An {} exception occured.'.format(e))


def predict(slctMvID):
    global oTrnFtr,oTrnLbl,oTstFtr
    print ("-ALGORITHM- Training model...")
    oPdctLbl=alg.run(oTrnFtr,oTrnLbl,oTstFtr)
    np.savetxt('result.txt',oPdctLbl)
    print ("-PREDICTION- Recording results...")
    sql= "UPDATE `data` SET `predict_1`=%f, `predict_2`=%f, `predict_3`=%f, `predict_4`=%f, `predict_5`=%f, `predict_6`=%f, `predict_7`=%f, `predict_8`=%f, `predict_9`=%f, `predict_10`=%f WHERE id = %s;"
    try:
        for i in range(oPdctLbl.shape[0]):
            cur.execute(sql % (oPdctLbl[i][0],oPdctLbl[i][1],oPdctLbl[i][2],oPdctLbl[i][3],oPdctLbl[i][4],oPdctLbl[i][5],oPdctLbl[i][6],oPdctLbl[i][7],oPdctLbl[i][8],oPdctLbl[i][9],slctMvID[i]))
            # cur.execute('UPDATE `data` SET `for` = "test" WHERE `id` = %s;',(slctMvID[i],))
        conn.commit()
    except Exception as e:
        print('-RECORD_RESULT- {}'.format(e))

def cal_metric(slctMvID):
    print('-CAL_METRIC- Calculating...')
    datee = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    real=[]
    predict=[]
    try:
        for mvID in slctMvID:
            cur.execute('SELECT `real_1`,`real_2`,`real_3`,`real_4`,`real_5`,`real_6`,`real_7`,`real_8`,`real_9`,`real_10` FROM `data` WHERE `id` = %s;',(mvID,))
            rstID = cur.fetchone()
            real=list(rstID.values())
            cur.execute('SELECT `predict_1`, `predict_2`, `predict_3`, `predict_4`, `predict_5`, `predict_6`, `predict_7`, `predict_8`, `predict_9`, `predict_10` FROM `data` WHERE `id` = %s;'
            ,(mvID,))
            rstID = cur.fetchone()
            predict=list(rstID.values())
            m=functions.k_l(predict,real)
            cur.execute('SELECT `title`,`year` FROM `data` WHERE `id` = %s;',(mvID,))
            rstID = cur.fetchone()
            text=functions.timestamp(predict,rstID)
            cur.execute('UPDATE `data` SET `stamp_text` = %s,`stamp_time` = %s,`metric` = %s WHERE `id` = %s;',(text,datee,m,mvID))
        conn.commit()
    except Exception as e:
        print('-CAL_METRIC- {}'.format(e))



def convert():
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
        (oneFtr, oneLbl) = o_generator.generate_matrices(mvID['id'],cur,conn,idxCtlg,lValue)
        if oTrnFtr is None:
            oTrnFtr = oneFtr
            oTrnLbl = oneLbl
        else:
            oTrnFtr = np.concatenate((oTrnFtr, oneFtr))
            oTrnLbl = np.concatenate((oTrnLbl, oneLbl))

    print ('-GENERATE_DATASET- Finished on generating train set.')

    # generate test set 
    cur.execute('SELECT `id` FROM `data` WHERE `for` = "show";')
    rstID = cur.fetchall()
    for mvID in rstID:
        slctMvID.append(mvID['id'])
        (oneFtr, oneLbl) = o_generator.generate_matrices(mvID['id'],cur,conn,idxCtlg,lValue)

        if oTstFtr is None:
            oTstFtr = oneFtr
            oTstLbl = oneLbl
        else:
            oTstFtr = np.concatenate((oTstFtr, oneFtr))
            oTstLbl = np.concatenate((oTstLbl, oneLbl))   

    print ('-GENERATE_DATASET- Finished on generating test set.')        
    # train the model
    predict(slctMvID)
    # calculate k-l distance
    cal_metric(slctMvID)



def run():
    global idxCtlg,lValue
    connect_to_sql()
    (idxCtlg,lValue)=o_generator.scan_column(cur,conn)
    convert()#old dataset
    conn.close()
if __name__ == '__main__':
    run()
