import pymysql
import numpy as np
import bfgslld as alg
# import p_generator
import o_generator
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
        print ('-PREDICTION- Connect to database successfully.')
    except Exception as e:
        print ('-- An {} exception occured.'.format(e))


def predict(slctMvID,prefix):
    global oTrnFtr,oTrnLbl,oTstFtr
    print ("-ALGORITHM- Training model...")
    oPdctLbl=alg.run(oTrnFtr,oTrnLbl,oTstFtr)
    print ("-PREDICTION- Recording results...")
    sql=''
    if prefix is 'o_':
        sql= "UPDATE `data` SET `o_predict_1`=%f, `o_predict_2`=%f, `o_predict_3`=%f, `o_predict_4`=%f, `o_predict_5`=%f, `o_predict_6`=%f, `o_predict_7`=%f, `o_predict_8`=%f, `o_predict_9`=%f, `o_predict_10`=%f WHERE id = %s;"
    else:
        sql= "UPDATE `data` SET `p_predict_1`=%f, `p_predict_2`=%f, `p_predict_3`=%f, `p_predict_4`=%f, `p_predict_5`=%f, `p_predict_6`=%f, `p_predict_7`=%f, `p_predict_8`=%f, `p_predict_9`=%f, `p_predict_10`=%f WHERE id = %s;"
    for i in range(oPdctLbl.shape[0]):
        cur.execute(sql % (oPdctLbl[i][0],oPdctLbl[i][1],oPdctLbl[i][2],oPdctLbl[i][3],oPdctLbl[i][4],oPdctLbl[i][5],oPdctLbl[i][6],oPdctLbl[i][7],oPdctLbl[i][8],oPdctLbl[i][9],slctMvID[i]))
        # cur.execute('UPDATE `data` SET `for` = "test" WHERE `id` = %s;',(slctMvID[i],))
    conn.commit()

def cal_metric(prefix,slctMvID):
    real=[]
    predict=[]
    for mvID in slctMvID:
        cur.execute('SELECT `real_1`,`real_2`,`real_3`,`real_4`,`real_5`,`real_6`,`real_7`,`real_8`,`real_9`,`real_10` FROM `data` WHERE `id` = %s;',(mvID,))
        rstID = cur.fetchone()
        real=list(rstID.values())
        if prefix is 'o_':
            cur.execute('SELECT `o_predict_1`, `o_predict_2`, `o_predict_3`, `o_predict_4`, `o_predict_5`, `o_predict_6`, `o_predict_7`, `o_predict_8`, `o_predict_9`, `o_predict_10` FROM `data` WHERE `id` = %s;'
            ,(mvID,))
        else:
            cur.execute('SELECT `p_predict_1`, `p_predict_2`, `p_predict_3`, `p_predict_4`, `p_predict_5`, `p_predict_6`, `p_predict_7`, `p_predict_8`, `p_predict_9`, `p_predict_10` FROM `data` WHERE `id` = %s;'
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
        if prefix is 'o_':
            (oneFtr, oneLbl) = o_generator.generate_matrices(mvID['id'],cur,conn,idxCtlg,lValue)
        # elif prefix is 'p_':
            # (oneFtr, oneLbl) = p_generator.generate_matrices(mvID['id'],cur,conn,idxCtlg,lValue)
        if oTrnFtr is None:
            oTrnFtr = oneFtr
            oTrnLbl = oneLbl
        else:
            oTrnFtr = np.concatenate((oTrnFtr, oneFtr))
            oTrnLbl = np.concatenate((oTrnLbl, oneLbl))

    print ('-GENERATE_DATASET- Finished on generating train set.')

    # generate test set 
    cur.execute('SELECT `id` FROM `data` WHERE `for` = "test";')
    rstID = cur.fetchall()
    for mvID in rstID:
        slctMvID.append(mvID['id'])
        if prefix is 'o_':
            (oneFtr, oneLbl) = o_generator.generate_matrices(mvID['id'],cur,conn,idxCtlg,lValue)
        # else prefix is 'p_':
        #     (oneFtr, oneLbl) = o_generator.generate_matrices(mvID['id'],cur,conn,idxCtlg,lValue)
        if oTstFtr is None:
            oTstFtr = oneFtr
            oTstLbl = oneLbl
        else:
            oTstFtr = np.concatenate((oTstFtr, oneFtr))
            oTstLbl = np.concatenate((oTstLbl, oneLbl))   

    print ('-GENERATE_DATASET- Finished on generating test set.')        
    # train the model
    predict(slctMvID,prefix)
    # calculate k-l distance
    cal_metric(prefix,slctMvID)



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
    conn.close()
if __name__ == '__main__':
    run()
