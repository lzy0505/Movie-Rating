function modelpara = ldsvrTrain(trainFeature, trainDistribution, para)
%LDSVRTRAIN	The training part of LDSVR algorithm.
%
%	Description
%   [MODELPARA] = LDSVRTRAIN(TRAINFEATURE, TRAINDISTRIBUTION, PARA) 
%   is the training part of LDSVR algorithm. 
%   The LDSVR deals with two challenges simultaneously: multivariate output and 
%   probability output. LDSVR uses MSVR to output multiple variables simultaneously 
%   and fit a sigmoid function to each component of the label distribution simultaneously. 
%
%	Inputs,
% 		TRAINFEATURE: training examples. [N, d]
%		TRAINDISTRIBUTION: training label distributions. [N, k]
% 		PARA: parameters needed for training
%
%   Outputs,
%       MODELPARA: parameters of the LDSVR model
%
%   Extended description of input/ouput variables
%   PARA,
%       PARA.TOL :  tolerance during the iteration
%   	PARA.EPSI : epsi-insensitive 
%       PARA.C :    penalty parameter
%       PARA.KER :  type of kernel function ('lin', 'poly', 'rbf', 'sam')
%       PARA.PAR :  parameters of kernel function
%           SIGMA:  width of the RBF and sam kernel
%           BIAS:   bias in the linear and polinomial kernel
%           DEGREE: degree in the polynomial kernel
%   MODELPARA,
%       MODELPARA.SVINDEX : support vectors' subscripts of row in trainFeature
%       MODELPARA.BETA : coeficient matrix of trainFeature's linear combination [N, k]
%       MODELPARA.B : intercept matrix [1, k]
%       MODELPARA.KER : type of kernel function, see PARA.KER
%       MODELPARA.PAR : parameter of kernel function, see PARA.PAR
%
%	See also
%	LLDPREDICT, LDSVRMSVR, KERNELMATRIX
%	
%   Copyright: Xin Geng (xgeng@seu.edu.cn)
%   School of Computer Science and Engineering, Southeast University
%   Nanjing 211189, P.R.China
%
fprintf('Begin training of LDSVR. \n');

%start training
[Beta,b,svindex] = ldsvrmsvr(trainFeature,trainDistribution,para);
%set the model parameters
modelpara.svindex = svindex;
modelpara.Beta = Beta;
modelpara.b = b;
modelpara.ker = para.ker;
modelpara.par = para.par;

end

