%LDSVRDEMO	The example of LDSVR algorithm.
%
%	Description  
%   We use MSVR to output multiple variables simultaneously and 
%   fit a sigmoid function to each component of the label distribution 
%   simultaneously. Here is an example of this LDSVR algorithm.
%
%	See also   
%   LDSVRPREDICT, LDSVRTRAIN
%
%   Copyright: Xin Geng (xgeng@seu.edu.cn)
%   School of Computer Science and Engineering, Southeast University
%   Nanjing 211189, P.R.China
%

clear;
clc;
% Load the trainData and ldsvrTestData. 
load o_movieDataSet;

% Initialize the model parameters.
para.tol  = 1e-10; %tolerance during the iteration
para.epsi = 0.01; %epsi-insensitive 
para.C    = 0.1; %penalty parameter
para.ker  = 'rbf'; %type of kernel function ('lin', 'poly', 'rbf', 'sam')
para.par  = 1*mean(pdist(trainFeature)); %parameter of kernel function

tic;
% The training part of LDSVR algorithm.
modelpara = ldsvrTrain(trainFeature,trainDistribution,para);
fprintf('Training time of LDSVR: %8.7f \n', toc);

% Prediction
 preDistribution = ldsvrPredict(testFeature, trainFeature, modelpara);
 fprintf('Finish prediction of LDSVR. \n');
 
 save o_predictDistribution preDistribution
 
% To visualize two distribution and display some selected metrics of distance
%for i=1:testNum
    % Show the comparisons between the predicted distribution
%	[disName, distance] = computeMeasures(testDistribution(i,:), preDistribution(i,:));
    % Draw the picture of the real and prediced distribution.
%    drawDistribution(testDistribution(i,:),preDistribution(i,:),disName, distance);
%end


