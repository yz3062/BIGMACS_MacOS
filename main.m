poolobj = parpool('local', 40);
fprintf('Number of workers: %g\n', poolobj.NumWorkers);

inputFile = 'R43';
inputMode = 'stack_construction';

BIGMACS(inputFile,inputMode,'show');

inputFile = 'R44';

BIGMACS(inputFile,inputMode,'show');

inputFile = 'R45';

BIGMACS(inputFile,inputMode,'show');
