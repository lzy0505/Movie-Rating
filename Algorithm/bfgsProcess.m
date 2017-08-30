function [target,gradient] = bfgsProcess(weights)
%BFGSPROCESS	Provide the target function and the gradient.
%
%	Description
%   [TARGET,GRADIENT] = BFGSPROCESS(WEIGHTS) provides the target function and the gradient.
%   They will be used in the optimization of BFGSLLD -- BFGSLLDTRAIN.
%   
%   Inputs,
%       WEIGHTS: the weights which will be optimized in BFGSLLDTRAIN
%   Outputs,
%       TARGET:  the target function which will be used in BFGSLLDTRAIN
%       GRADIENT: the gradient which will be used in BFGSLLDTRAIN
% 
%	See also
%	BFGSLLDTRAIN, LLDPREDICT, FMINLBFGS 
%	
%   Copyright: Xin Geng (xgeng@seu.edu.cn)
%   School of Computer Science and Engineering, Southeast University
%   Nanjing 211189, P.R.China
%

% Load the data set.
load o_movieDataSet;

% lambda=0.5;
modProb = exp(trainFeature * weights);  % size_sam * size_Y
sumProb = sum(modProb, 2);
modProb = modProb ./ (repmat(sumProb,[1 size(modProb,2)]));

% Target function.
target = -sum(sum(trainDistribution.*log(modProb)));

% The gradient.
gradient = trainFeature'*(modProb - trainDistribution);

end
