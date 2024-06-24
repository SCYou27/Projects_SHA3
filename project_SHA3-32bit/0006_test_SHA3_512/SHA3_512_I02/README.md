# Attack experiment with 2-invocational SHA3-512 inputs

The main goal of the tasks in "0006\_test\_SHA3\_512/SHA3\_512\_I02/" is to test how our attack performs on the 2-invocational SHA3-512 hash function.

1. Please download the raw traces used in this phase from the following website:

	https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0006_test_SHA3_512/

   Alternatively, go to the directory "Raw/" to execute the script to download the raw traces:

	`cd Raw/`  
	`./script_all.sh`  

2. Trace pre-processing:

	`cd Code_preprocessing/`  
	`./script_all.sh`  

   This step will check the quality of the raw traces in this phase against the reference trace ("../0001\_referece/Code\_reference/ref\_trace.npy"), and then extract the I/O data in the archived raw trace ZIP files.

   The processed trace will be stored in an independent directory "0006_test_SHA3_512/Processed_HDF5/" as 2 HDF5 files, each containing 1000 traces, categorized by the invocations of permutation.

3. Intermeidate value calculation:

	`cd Code_intermediate_values/`  
	`./script_all.sh`  

   Based on the extracted I/O data, this step will calculate our target intermediate values and store them in bits (binary variables) for the multiple linear regression in the later detections.

4. Find the pieces of traces with given interesting clock cycle sets:

	`cd Code_find_IoPs/`  
	`./script_all.sh`  

   After downsampling, the resampled traces contain 10 samples for each clock cycle in the window for recording. This step is to concatenate the samples of the interesting clock cycles into a reassembled trace in files such as "Code_find_IoPs/IoPs/Ints_A00_i00.hdf5". This means that when the interesting clock cycle set for a target intermediate 32-bit word contains indices [0, 10, 15, 17], we will select samples 0, 1, ..., 9, 100, 101, ..., 109, 150, 151, ..., 159, 170, 171, ..., 179 from the downsampled trace, concatenate them to form a newly reassembled trace, and then store it in the HDF5 files. As a result, the length of the traces in "Ints_A00_i00.hdf5" is 10 times the number of the interesting clock cycles for the first 32-bit word in state A00, for example. 

5. Template profiling:

	`cd template_profiling_bytes/`  
	`./script_all.sh`  

   This step is to build templates with multiple linear regression and linear discriminant analysis (LDA). The resulting templates will be stored in "template_profiling_bytes/templateLDA_O010.zip"



