function modProb = lldPredict(weights, x)
%LLDPREDICT	Calculate the predicted distribution of the instance X by weights.
%
%	Description
%   MODPROB = LLDPREDICT(WEIGHTS, X) calculate the predicted distribution
%   of the instance X by weights.
%
%   Inputs,
%       WEIGHTS: the weights(parameters) trained by LDL model.
%       X: testFeature.
%
%   Outputs,
%       MODPROB: the prediction of label distribution.
%
%	See also
%	IISLLDTRAIN, BFGSLLDTRAIN
%	
%   Copyright: Xin Geng (xgeng@seu.edu.cn)
%   School of Computer Science and Engineering, Southeast University
%   Nanjing 211189, P.R.China
%

fprintf('begin to predict using IIS-LLD / BFGS-LLD.\n');
modProb = exp(x * weights);
sumProb = sum(modProb, 2); % sum of rows
modProb = scalecols(modProb, 1 ./ sumProb);

function modProb = scalecols(x, s)
[numRows, numCols] = size(x); 
modProb = x .* repmat(s, 1, numCols);

