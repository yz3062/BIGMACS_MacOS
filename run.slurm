#!/bin/bash
#SBATCH -c 6 # Use more cores
#SBATCH --time=24:00:00 # Request an hour of runtime
#SBATCH -p shared
#SBATCH --mem-per-cpu=4G # Use more memory
#SBATCH -J DNEA # Specify a job name

# Specify an output file
#SBATCH -o DNEA.out
#SBATCH -e DNEA.out

# Run a command

module load matlab/R2021a-fasrc01

matlab -nojvm -nosplash -nodesktop -r "main; exit"