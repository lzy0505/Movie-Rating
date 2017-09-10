import math
def four_five(sum):
    sum=str(sum*1000)
    if(int(sum[sum.index('.')+1])>4):
        sum=str(float(sum)+1)  
    sum=sum[0:sum.index('.')]
    sum=str(int(sum)/1000.0)
    while (len(sum)-1-sum.index('.')<3):
        sum+='0'
    return sum


def cheby(pre,real):
    max=0.0
    for i in xrange(0,10):
        if(abs(pre[i]-real[i])>max):
            max=abs(pre[i]-real[i])
    return four_five(max)

def clark(pre,real):
    sum=0.0
    for i in xrange(0,10):
         sum+=((pre[i]-real[i])**2/(pre[i]+real[i])**2)
    return four_five(math.sqrt(sum))

def cbra(pre,real):
    sum=0.0
    for i in xrange(0,10):
         sum+=(abs(pre[i]-real[i])/(pre[i]+real[i]))
    return four_five(sum)

def k_l(pre,real):
    sum=0.0
    for i in xrange(0,10):
        sum+=(pre[i]*math.log(pre[i]/real[i]))
    return four_five(sum)

def cos(pre,real):
    sum_n=0.0
    sum_dp=0.0
    sum_dr=0.0
    for i in xrange(0,10):
         sum_n+=pre[i]*real[i]
         sum_dp+=pre[i]*pre[i]
         sum_dr+=real[i]*real[i]
    return four_five(sum_n/(math.sqrt(sum_dp)*math.sqrt(sum_dr)))

def intsc(pre,real):
    sum=0.0
    for i in xrange(0,10):
        if(pre[i]>real[i]):
            sum+=real[i]
        else:
            sum+=pre[i]
    return four_five(sum)


def cal(pre,real):
    indexs={}
    indexs['cheby']=cheby(pre,real)
    indexs['clark']=clark(pre,real)
    indexs['cbra']=cbra(pre,real)
    indexs['k-l']=k_l(pre,real)
    indexs['cos']=cos(pre,real)
    indexs['intsc']=intsc(pre,real)
    return indexs


