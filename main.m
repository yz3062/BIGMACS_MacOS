poolobj = parpool('local', 40);
fprintf('Number of workers: %g\n', poolobj.NumWorkers);

inputFile = 'R9';

% inputMode = 'age_model_construction';
inputMode = 'stack_construction';

BIGMACS(inputFile,inputMode,'show');
