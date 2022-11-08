poolobj = parpool('local', 40);
fprintf('Number of workers: %g\n', poolobj.NumWorkers);

inputFile = 'R11';

% inputMode = 'age_model_construction';
inputMode = 'stack_construction';
tic
BIGMACS(inputFile,inputMode,'show');
toc
