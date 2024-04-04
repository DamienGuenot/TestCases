#!/bin/bash
RUN_MACH_PYTHON="as_opt.py" #Was struct_opt2_as_run_cruise2.py
RUN_MACH_SHELL="run_mach.sh" #Was run_mach_struct_opt_as_run2.sh
# Delete result_MACH.json from the previous iteration

# Keep the main.py absolute path
abs_main=$(pwd)

# Define high-level variables: number of processors, name of result direcory
nb_proc=4 #128
output_MACH="output_as_opt"
lsf_submit="NO"


DIRORI=$PWD
cd $DIRORI

cp ./template_lsf_options ./heuristic_MACH_default
command_line="python3 $RUN_MACH_PYTHON --output $output_MACH"
if [[ x$lsf_submit == "xYES" ]]; then
	echo "LSF submission"
	echo "$command_line"
	SubmitMach --np=$nb_proc --machversion=2.0.0 --estruntime=15:00 --appoptions="python3 $RUN_MACH_PYTHON --output $output_MACH"
else
	/opt/soft/cdtng/tools/mach/2.0.0/bin/activate
	. /opt/soft/cdtng/tools/mach/2.0.0/envs/mach/etc/profile.d/conda.sh 
	conda activate /opt/soft/cdtng/tools/mach/2.0.0/envs/mach
	mpirun -np $nb_proc $command_line > $RUN_MACH_PYTHON.log 2>&1
fi
