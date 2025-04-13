function [QQ] = initializeAlignment(data,data_ps,param,target,setting)

L = length(data);
data_type = setting.data_type;

QQ = cell(L,1);
parfor ll = 1:L
% parfor (ll = 1:L, 0)
    QQ{ll} = getProposal(data(ll),data_ps(ll),param,target,data_type);
end


end