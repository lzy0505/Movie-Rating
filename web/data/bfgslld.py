import scipy as sp
import scipy.optimize as spopt
import numpy as np

# trnFtr,trnLbl,tstFtr


def process(weights):
	global trnFtr,trnLbl
	weights = np.reshape(weights,(trnFtr.shape[1],trnLbl.shape[1]))
	modPbblt = np.exp(trnFtr.dot(weights))
	sumPbblt = np.sum(modPbblt,axis=1)
	sumPbblt = np.reshape(sumPbblt,(sumPbblt.shape[0],1))
	modPbblt = modPbblt/np.tile(sumPbblt,(1,modPbblt.shape[1]))
	return modPbblt

def target(weights):
	global trnFtr,trnLbl
	modPbblt = process(weights)
	tgt = -np.sum(np.sum(trnLbl*np.log(modPbblt)))
	return tgt

def gradient(weights):
	global trnFtr,trnLbl
	modPbblt = process(weights)
	gdt = trnFtr.transpose().dot((modPbblt - trnLbl))
	gdt=np.hstack(gdt)
	return gdt

def train(init):
	(xopt,fopt,others)=spopt.fmin_l_bfgs_b(target,init,gradient,maxiter =400)
	print "Gradient:%s\nwarnflag:%d" % (others['grad'],others['warnflag'])
	return (xopt,fopt)

def predict(weights, x):
	weights = np.reshape(weights,(trnFtr.shape[1],trnLbl.shape[1]))
	modPbblt = np.exp(x.dot(weights))
	sumPbblt = np.sum(modPbblt,axis=1)
	sumPbblt = np.reshape(sumPbblt,(sumPbblt.shape[0],1))
	modPbblt = modPbblt*np.tile(1/sumPbblt,(1,modPbblt.shape[1]))
	# print modPbblt.shape
	return modPbblt



def run(trnF,trnL,*tstF):
	global trnFtr,trnLbl,tstFtr
	trnFtr = trnF
	trnLbl = trnL
	item = np.eye(trnFtr.shape[1],trnLbl.shape[1])
	# print item.shape
	(weights,fval)=train(item)
	print "Finished training"	
	if len(tstF)==1:
		tstFtr = tstF[0]
		pdctLbl=predict(weights,tstFtr)
		print "Finished prediction"
		return pdctLbl
