function K = kernelmatrix(ker, parameter, testFeature, trainFeature)
% KERNELMATRIX calculate the kernel matrix of instance vectors in testFeature and trainFeature.
%
%	Description
%   K = KERNELMATRIX(KER, X, trainFeature, PARAMETER) calculate the kernel 
%   matrix of the instance vectors in testFeature and trainFeature.
%   The function we writed is based on the original kernelmatrix function 
%   writed by Gustavo Camps-Valls(2006(c)) and updated by Jordi(jordi@uv.es,2007-11).
%
%   Inputs,
%       KER:          type of kernel function ('lin', 'poly', 'rbf', 'sam')
%       PARAMETER:    parameters of kernel function
%       TESTFEATURE:  data matrix with training samples in columns and features in rows (d x m)
%       TRAINFEATURE: data matrix with test samples in columns and features in in rows (d x c)
%
%   Outputs,
%       K:  kernel matrix, each element corresponds to the kernel of two feature vectors (c x m)
%
%   Extended description of input/ouput variables
%       PARAMETER:
%           SIGMA:  width of the RBF and sam kernel
%           BIAS:   bias in the linear and polinomial kernel
%           DEGREE: degree in the polynomial kernel
%
%   Copyright: Xin Geng (xgeng@seu.edu.cn)
%   School of Computer Science and Engineering, Southeast University
%   Nanjing 211189, P.R.China
%
switch ker
    case 'lin'
        if exist('trainFeature','var')
            K = testFeature' * trainFeature + parameter;
        else
            K = testFeature' * testFeature + parameter;
        end

    case 'poly'
        if exist('trainFeature','var')
            K = (testFeature' * trainFeature + 1).^parameter;
        else
            K = (testFeature' * testFeature + 1).^parameter;
        end
        
    %To speed up the computation of the RBF kernel matrix, 
    %we exploit a decomposition of the Euclidean distance (norm).
    case 'rbf'  
        n1sq = sum(testFeature.^2,1); %compute x^2
        n1 = size(testFeature,2);
        if isempty(trainFeature);
            %||x-y||^2 = x^2 + y^2 - 2*x'*y 
            D = (ones(n1,1)*n1sq)' + ones(n1,1)*n1sq -2*testFeature'*testFeature;
        else
            n2sq = sum(trainFeature.^2,1);
            n2 = size(trainFeature,2);
            %||x-y||^2 = x^2 + y^2 - 2*x'*y 
            D = (ones(n2,1)*n1sq)' + ones(n1,1)*n2sq -2*testFeature'*trainFeature; 
        end;
        K = exp(-D/(2*parameter^2));

    case 'sam'
        if exist('trainFeature','var');
            D = testFeature'*trainFeature;
        else
            D = testFeature'*testFeature;
        end
        K = exp(-acos(D).^2/(2*parameter^2));

    otherwise
        error(['Unsupported kernel ' ker])
end
