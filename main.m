%poolobj = parpool('local', 40);
%fprintf('Number of workers: %g\n', poolobj.NumWorkers);

inputFile = 'R79';

inputMode = 'age_model_construction';

BIGMACS(inputFile,inputMode,'show');
