function predict = ldsvrPredict(testFeature, trainFeature, modelpara)
%LDSVRPREDICT	 prediction part of the  LDSVR model.
%
%	Description
%   PREDICT = LDSVRPREDICT(TESTFEATURE, MODELPARE, TRAINFEATURE)  
%   predicts the distribution of test data using the trained LDSVR model..
%
%   Inputs,
%       TESTFEATURE:  data matrix with test samples in rows and features in columns [M, d]
%       TRAINFEATURE: data matrix with training samples in rows and features in columns [N, d]
%       MODELPARA:    model parameters of LDSVR model.
%
%   Outputs,
%       PREDICT:      prediction of testFeature's label distribution.
%
%   Extended description of input/ouput variables
%   MODELPARA,
%       MODELPARA.SVINDEX : support vectors' subscripts of row in trainFeature
%       MODELPARA.BETA :    coeficient matrix of trainFeature's linear combination [N, k]
%       MODELPARA.B :       intercept matrix [1, k]
%       MODELPARA.KER :     type of kernel function ('lin', 'poly', 'rbf', 'sam')
%       MODELPARA.PAR :     parameters of kernel function
%           SIGMA:  width of the RBF and sam kernel
%           BIAS:   bias in the linear and polinomial kernel
%           DEGREE: degree in the polynomial kernel
%
%	See also
%   LDSVRTRAIN, MSVR, KERNELMATRIX	
%
%   Copyright: Xin Geng (xgeng@seu.edu.cn)
%   School of Computer Science and Engineering, Southeast University
%   Nanjing 211189, P.R.China
%

fprintf('begin to predict using LDSVR.\n');
%Compute kernel matrix for prediction using testFeature and trainFeature
Ktest = kernelmatrix(modelpara.ker, modelpara.par, testFeature',trainFeature');
%Prediction.
predict = Ktest*modelpara.Beta+repmat(modelpara.b,size(Ktest,1),1); 
%Use sigmoid function to the predicted label distribution.
predict = 1./(1+exp(-predict));
%Normalization for the predicted label distribution.
predict = predict./repmat(sum(predict,2),1,size(predict,2));  
end
