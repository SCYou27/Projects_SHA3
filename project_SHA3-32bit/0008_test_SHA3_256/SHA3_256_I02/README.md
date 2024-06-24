# Attacks to recover 2-invocational SHA3-256 inputs

The main goal of the tasks in "0008\_test\_SHA3\_256/SHA3\_256\_I02/" is to test how our attack performs on the 2-invocational SHA3-256 hash function.

1. Please download the raw traces used in this phase from the following website:

	https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0008_test_SHA3_256/index.html#I02

   Alternatively, go to the directory "Raw/" to execute the script to download the raw traces:

	`cd Raw/`  
	`./script_all.sh`  

2. Trace pre-processing:

	`cd Code_preprocessing/`  
	`./script_all.sh`  

   This step will check the quality of the raw traces in this phase against the reference trace ("../0001\_referece/Code\_reference/ref\_trace.npy"), and then extract the I/O data in the archived raw trace ZIP files.

   The processed trace will be stored in an independent directory "0008\_test\_SHA3\_256/SHA3\_256\_I02/Processed\_HDF5/" as 2 HDF5 files, each containing 1000 traces, categorized by the invocations of permutation.

3. Hash function input recovery:

	`cd template_attack_SHA3_256_4R_I02/` (or `template_attack_SHA3_256_3R_I02/`, `template_attack_SHA3_256_2R_I02`, `template_attack_SHA3_256_1R_I02/`)  
	`./script_all.sh`  

   The result will be recorded in the file "report.txt", which contains the number of successfully recovered inputs out of the 1000 trials and statistics (mean, median, maximum) of iterations required for the loopy-BP procedure to stabilize.
