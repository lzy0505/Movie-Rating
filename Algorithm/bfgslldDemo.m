%BFGSLLDDEMO	The example of BFGSLLD algorithm.
%
%	Description
%   In order to optimize the IIS-LLD algorithm, we follow the idea of an
%   effective quasi-Newton method BFGS to further improve IIS-LLD. 
%   Here is an example of BFGSLLD algorithm.
%	
%	See also
%	LLDPREDICT, BFGSLLDTRAIN
%	
%   Copyright: Xin Geng (xgeng@seu.edu.cn)
%   School of Computer Science and Engineering, Southeast University
%   Nanjing 211189, P.R.China
%
clear;
clc;
% Load the trainData and TestData.
load o_movieDataSet;

item=eye(size(trainFeature,2),size(trainDistribution,2));

% The training part of BFGSLLD algorithm.
tic;
% The function of bfgsprocess provides a target function and the gradient.
[weights,fval] = bfgslldTrain(@bfgsProcess,item);
fprintf('Training time of BFGS-LLD: %8.7f \n', toc);

% Prediction
preDistribution = lldPredict(weights,testFeature);
fprintf('Finish prediction of BFGS-LLD. \n');

save b_o_predictDistribution preDistribution

% To visualize two distribution and display some selected metrics of distance
%for i=1:testNum
    % Show the comparisons between the predicted distribution
%	[disName, distance] = computeMeasures(testDistribution(i,:), preDistribution(i,:));
    % Draw the picture of the real and prediced distribution.
 %   drawDistribution(testDistribution(i,:),preDistribution(i,:),disName, distance);
    %sign=input('Press any key to continue:');
%end
