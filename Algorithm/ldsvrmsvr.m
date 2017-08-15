function [Beta, b, svindex] = ldsvrmsvr(x, y, para)
%LDSVRMSVR	LDSVR's Multioutput SVR
%
%	Description
%   [BETA, B, SVINDEX] = LDSVRMSVR(X, Y, PARA) is the LDSVR's Multioutput SVR
%   
%   Statement
%   The function [Beta, b, svindex] = ldsvrmsvr(x, y, para) we writed is adapted
%   from the original function msvr wrote by Fernando Pérez Cruz. 
%   we modify it to fit the original msvr into LDSVR framework. Compared with the former, 
%   the main change is that we pre-proccess the trainDistribution required by LDSVR before 
%   training, as well as add the parameter b and substitute u by u_z.
%
%   Inputs,
%       X :      data matrix with training samples in rows and features in in columns [N, d]
%       Y :      label distribution matrix Corresponds to the training samples in X above [N, k]
%       PARA :   model parameters of LDSVR model.
%
%   Outputs,
%       BETA :    coeficient matrix of trainFeature's linear combination [N, k]
%       B :       intercept matrix [1, k]
%       SVINDEX : support vectors' subscripts of row in trainFeature
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
%
%	See also
%   LDSVRTRAIN, KERNELMATRIX, LDSVRPREDICT
%
%   Copyright: Xin Geng (xgeng@seu.edu.cn)
%   School of Computer Science and Engineering, Southeast University
%   Nanjing 211189, P.R.China
%


%Pre-proccess the trainDistribution
n_k = size(y,2);
zero = find(y==0);
y(zero) = y(zero) + 1/(n_k*10); %avoid the error of dividing zero
y = y ./ repmat(sum(y')',1,n_k); %normalization
y = -log(1./y - 1); %use sigmoid function to the trainDistribution   

N=size(x,1); %count of training samples
n_k=size(y,2); %dimension of the label distribution

% default value of para
% para.tol=10^-20;
% para.epsi = 1;
% para.C = 1;
% para.par = 0.01;
% para.ker = 'rbf';

%build the kernel matrix on the labeled samples (N x N)
H = kernelmatrix(para.ker, para.par, x', x');

%create matrix for regression parameters
Beta = zeros(N, n_k); %w(j) may be represented as a linear combination of the training examples in the feature space   
b = zeros(1, n_k); 

%prediction error matrix (N x k)
E = y-H*Beta-repmat(b, N, 1);  
%compute prediction error's Euclidean distance for each examples
u = sqrt(sum(E.^2,2)); %u = RSE (N x 1)
u_z = u / 4; %use u_z to substitute  u_d

%RMSE
RMSE(1,1) = sqrt(mean(u_z.^2));

%points for which prediction error is larger than epsilon, i.e., find SVs whose loss function != 0
i1 = find(u_z>=para.epsi);

%set initial values of alphas (N x 1)
a = para.C*(u_z-4*para.epsi)./(4*u_z);

%compute loss function matrix by definition
L = zeros(size(u_z)); % L is the loss function matrix (N x 1)  
%we modify only entries for which  u_z > epsi.
L(i1) = u_z(i1).^2-2*para.epsi*u_z(i1)+para.epsi^2;   

%Lp is the quantity to minimize (sq norm of parameters + slacks)
Lp(1,1) = sum(diag(Beta'*H*Beta))/2+para.C*sum(L);

%initial variables used in loop
eta=1; %step length
k=1; %iteration number
hacer=1; %sentinel of loop
val=1; %sign of whether find support vectors

%strat training
while(hacer)
    
    % Print the iteration information.
    fprintf('iter:%4d, Lp:%15.7f, RMSE:%15.7f\n', k, Lp(k,1), RMSE(k,1));
    
    %next iteration
    k = k+1; 
    
    %save the model parameters in the previous step
    Beta_a = Beta;
    b_a = b;
    i1_a = i1;
    
    %[H+inv(D_a), 1; a'*H, 1'*a]*[Beta(:j), b(j)] = [y(:j), a'*y(:j)] 
    %M1 = [H+inv(D_a), 1; a'*H, 1'*a] (only for obs i1. see above)   
    M1 = [H(i1,i1)+diag(1./a(i1))];
    M1 = [M1 ones(size(M1,1),1)];
    temp = [a(i1)'*H(i1,i1) sum(a(i1))];
    M1 = [M1;temp];
    M1 = M1+1e-11*eye(size(M1,1));

    %compute Beta and b (only for obs i1. see above)   
    sal1 = inv(M1)*[y(i1,:);(a(i1)'*y(i1,:))];
    b_sal1 = sal1(end,:);
    b = b_sal1;
    sal1 = sal1(1:end-1,:);
    Beta = zeros(size(Beta));
    Beta(i1,:) = sal1;
    
    %recompute error
    E=y-H*Beta-repmat(b,N,1);
    %recompute i1 and u_z
    u=sqrt(sum(E.^2,2));
    u_z = u / 4;
    i1=find(u_z>=para.epsi);
    %recompute loss function 
    L=zeros(size(u_z));
    L(i1)=u_z(i1).^2-2*para.epsi*u_z(i1)+para.epsi^2;
    %computer Lp in kth iteration 
    Lp(k,1)=sum(diag(Beta'*H*Beta))/2+para.C*sum(L);

    eta=1; %initial step length
    %Loop where we keep alphas and modify betas
    while(Lp(k,1)>Lp(k-1,1))
        
        eta=eta/10; %modify step length
        i1=i1_a; %restore i1
        
        %the new betas are a combination of the current (sal1) and of the
        %previous iteration (Beta_a)
        Beta=zeros(size(Beta));
        Beta(i1,:)=eta*sal1+(1-eta)*Beta_a(i1,:);
        b=eta*b_sal1+(1-eta)*b_a;
        
        %recoumpte
        E=y-H*Beta-repmat(b,N,1);
        u_z=sqrt(sum(E.^2,2));
        u_z = u_z / 4;
        i1=find(u_z>=para.epsi);
        
        L=zeros(size(u_z));
        L(i1)=u_z(i1).^2-2*para.epsi*u_z(i1)+para.epsi^2;
        %recomputer Lp in kth iteration 
        Lp(k,1)=sum(diag(Beta'*H*Beta))/2+para.C*sum(L);
        
        %stopping criterion #1
        if(eta<10^-16)
            fprintf('stop criterion 1: meet eta(step length) condition -> eta<10^-16.\n');
            Lp(k,1)=Lp(k-1,1)-10^-15;
            %save parameters
            Beta=Beta_a;
            b=b_a;
            i1 = i1_a;
            hacer=0; %stop loop
        end
    end
    
    %here we modify the alphas
    a_a=a;
    a = para.C*(u_z-4*para.epsi)./(4*u_z);
    %computer RMSE in kth iteration
    RMSE(k,1) = sqrt(mean(u_z.^2));

    %stopping criterion #2
    if((Lp(k-1,1)-Lp(k,1))/Lp(k-1,1) < para.tol)
        fprintf('stop criterion 2: meet tolerance condition -> Lp(k-1,1)-Lp(k,1))/Lp(k-1,1)<tol\n');
        % Beta = Beta;
        % b = b;
        % i1 = i1;
        hacer = 0; %stop loop
    end

    %stopping criterion #3 - algorithm does not converge. (val = -1)   
    if(isempty(i1))
        fprintf('stop criterion 3: algorithm does not converge (find no SVs).\n');    
        Beta = zeros(size(Beta));
        b = zeros(size(b));
        i1 = [];
        val = -1;
        hacer=0; %stop loop
    end
        
end

svindex = i1;

end

