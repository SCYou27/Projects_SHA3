# Reference traces

Reference: the main goal of tasks in "0001_reference/" is to generate a reference trace (ref_trace.npy) for trace quality control in the next phases.

1. Please download the raw traces used in this phase from the following website:

	https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0001_reference/

   Alternatively, go to the directory "Raw/" to execute the script to download the raw traces:

	`cd Raw/`  
	`./script_all.sh`  

2. Reference trace calculation:

	`cd Code_reference/`  
	`./script_all.sh`  

   The resulting mean trace "Code_reference/ref_trace.npy" will be used in the trace pre-processing steps in the later phases.


