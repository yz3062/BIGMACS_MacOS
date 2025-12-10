% poolobj = parpool('local', 36);
% fprintf('Number of workers: %g\n', poolobj.NumWorkers);

inputFile = 'R120';

inputMode = 'age_model_construction';

BIGMACS(inputFile,inputMode,'show');