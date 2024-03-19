%poolobj = parpool('local', 36);
%fprintf('Number of workers: %g\n', poolobj.NumWorkers);

inputFile = 'Eocene_Diego';

inputMode = 'stack_construction';

BIGMACS(inputFile,inputMode,'show');
