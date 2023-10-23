poolobj = parpool('local', 36);
fprintf('Number of workers: %g\n', poolobj.NumWorkers);

inputFile = 'R87';

inputMode = 'stack_construction';

BIGMACS(inputFile,inputMode,'show');
