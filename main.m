poolobj = parpool('local', 10);
fprintf('Number of workers: %g\n', poolobj.NumWorkers);

inputFile = 'R56';

inputMode = 'stack_construction';

BIGMACS(inputFile,inputMode,'show');
