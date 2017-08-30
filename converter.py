import numpy as np
import scipy.io as sio
import random

my_sql_table='future_movies'

if my_sql_table=='future_movies':
    trainFeature=np.loadtxt('info.txt',dtype='double')
    testFeature=np.loadtxt('f_info.txt',dtype='double')
    trainDistribution=np.loadtxt('rating.txt',dtype='double')
    testDistribution=[]
    (r,c)=trainFeature.shape
    trainNum=r
    (r,c)=testFeature.shape
    testNum=r

    print trainFeature.shape
    print trainDistribution.shape
    print testFeature.shape

    sio.savemat('f_movieDataSet.mat',{'testDistribution':testDistribution,'testFeature':testFeature,'testNum':testNum,'trainDistribution':trainDistribution,'trainFeature':trainFeature,'trainNum':trainNum})
elif my_sql_table=='new_movies':
    num_of_partition=10
    f=np.loadtxt('info.txt',dtype='double')
    d=np.loadtxt('rating.txt',dtype='double')

    selected_index=[]

    pre_index=0
    now_index=random.randint(1,num_of_partition+1)
    selected_index.append(now_index)
    trainFeature=f[pre_index:now_index]
    trainDistribution=d[pre_index:now_index]
    testFeature=f[now_index:now_index+1]
    testDistribution=d[now_index:now_index+1]
    pre_index=now_index+1
    # print now_index

    (r,c)=f.shape


    for i in xrange(1,int(r/num_of_partition)):
        now_index=random.randint(i*num_of_partition,(i+1)*num_of_partition+1)
        selected_index.append(now_index)
        trainFeature=np.concatenate((trainFeature,f[pre_index:now_index]))
        trainDistribution=np.concatenate((trainDistribution,d[pre_index:now_index]))
        testFeature=np.concatenate((testFeature,f[now_index:now_index+1]))
        testDistribution=np.concatenate((testDistribution,d[now_index:now_index+1]))
        pre_index=now_index+1
        
    
    trainFeature=np.concatenate((trainFeature,f[pre_index:]))
    trainDistribution=np.concatenate((trainDistribution,d[pre_index:]))

    (r,c)=trainFeature.shape
    trainNum=r
    (r,c)=testFeature.shape
    testNum=r

    print f.shape
    print trainFeature.shape
    print trainDistribution.shape
    print testFeature.shape
    print testDistribution.shape
    print trainNum+testNum

    sio.savemat('o_movieDataSet.mat',{'testDistribution':testDistribution,'testFeature':testFeature,'testNum':testNum,'trainDistribution':trainDistribution,'trainFeature':trainFeature,'trainNum':trainNum,'testIndex':selected_index})

    