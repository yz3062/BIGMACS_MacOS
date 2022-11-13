poolobj = parpool('local', 36);
fprintf('Number of workers: %g\n', poolobj.NumWorkers);

inputFile = 'R11';

% inputMode = 'age_model_construction';
inputMode = 'stack_construction';
BIGMACS(inputFile,inputMode,'show');
