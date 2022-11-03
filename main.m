<<<<<<< HEAD
%poolobj = parpool('local', 36);
%fprintf('Number of workers: %g\n', poolobj.NumWorkers);
=======
poolobj = parpool('local', 40);
fprintf('Number of workers: %g\n', poolobj.NumWorkers);
>>>>>>> cc8b1a6f9510e79d22e7d616b70d8f6ec70fb810

inputFile = 'R10';

% inputMode = 'age_model_construction';
inputMode = 'stack_construction';

BIGMACS(inputFile,inputMode,'show');
