% poolobj = parpool('local', 36);
% fprintf('Number of workers: %g\n', poolobj.NumWorkers);

inputFile = 'R97';

inputMode = 'age_model_construction';

BIGMACS(inputFile,inputMode,'show');
