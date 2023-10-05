%poolobj = parpool('local', 40);
%fprintf('Number of workers: %g\n', poolobj.NumWorkers);

inputFile = 'R78';

inputMode = 'stack_construction';

BIGMACS(inputFile,inputMode,'show');
