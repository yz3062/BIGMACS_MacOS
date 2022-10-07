#!/bin/bash

# This script doesn't need to run on a batch node... we can simply submit
# the parallel job by running this script on the login node

module rm ncarenv
module load matlab

# Job parameters
MPSNODES=1
MPSTASKS=20
MPSACCOUNT=UCSB0015
MPSQUEUE=casper@casper-pbs
MPSWALLTIME=12:00:00
SECONDS=0

matlab -nodesktop -nosplash << EOF
% Add cluster profile if not already present
if ~any(strcmp(parallel.clusterProfiles, 'ncar_mps'))
    ncar_mps = parallel.importProfile('/glade/u/apps/opt/matlab/parallel/ncar_mps.mlsettings');
end

% Start PBS cluster and submit job with custom number of workers
c = parcluster('ncar_mps');

% Matlab workers will equal nodes * tasks-per-node - 1
jNodes = '$MPSNODES';
jTasks = '$MPSTASKS';
jWorkers = str2num(jNodes) * str2num(jTasks) - 1;

c.ClusterMatlabRoot = getenv('NCAR_ROOT_MATLAB');
c.ResourceTemplate = append('-l select=', jNodes, ':ncpus=', jTasks, ':mpiprocs=', jTasks);
c.SubmitArguments = append('-A $MPSACCOUNT -q $MPSQUEUE -l walltime=$MPSWALLTIME');
c.JobStorageLocation = append(getenv('PWD'), '/Outputs');

% Output cluster settings
c

% Submit job to batch scheduler (PBS)
j = c.batch('main', 'pool', jWorkers);

% Wait for job to finish and get output
wait(j);
diary(j);
exit;
EOF

echo "Time elapsed = $SECONDS s"
