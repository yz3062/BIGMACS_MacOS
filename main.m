poolobj = parpool('local', 40);
fprintf('Number of workers: %g\n', poolobj.NumWorkers);

inputFile = 'R101';

inputMode = 'stack_construction';

BIGMACS(inputFile,inputMode,'show');
