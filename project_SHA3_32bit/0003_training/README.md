# Profiling (training) traces

Profiling (Training): the main goal of tasks in "0003_training/" is to build the templates used in our attacks.

1. Please download the raw traces used in this phase from the following website:

	https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0003_training/

   Alternatively, just go to the directory "Raw/" to execute the script to download the raw traces:

	>> cd Raw/
	>> ./script_all.sh

2. Trace pre-processing:

	>> cd Code_preprocessing/
	>> ./script_all.sh

   This step will check the quality of the raw traces in this phase against the reference trace ("0001_referece/Code_reference/ref_trace.npy"), and also extract the I/O data in the archived raw trace ZIP files.

   The processed trace will be stored in an independent directory "0003_training/Processed_HDF5/" as 16 HDF5 files, where each contains 4000 traces.

3. Intermeidate value calculation:

	>> cd Code_intermediate_values/
	>> ./script_all.sh

   Based on the extracted I/O data, this step is to calculate our target intermediate values and store them in bits (binary variables) for the multiple linear regression in the later detections.

4. Find the pieces of traces with given interesing clock cycle sets:

	>> cd Code_find_IoPs/
	>> ./script_all.sh

   After downsampling, the resampled traces contain 10 samples for each clock cycle in the window for recording. This step is to concatenate the samples of the interesting clock cycles into a reassembled trace in files such as "Code_find_IoPs/IoPs/Ints_A00_i00.hdf5". This means, when the interesting clock cycle set for a target intermediate 32-bit word contains indices [0, 10, 15, 17],  we will concatenate a point 0, 1, ..., 9, 100, 101, ..., 109, 150, 151, ..., 159, 170, 171, ..., 179 from the downsampled trace and concatenate all these points into a newly reassembled trace in the HDF5 files. For example, you can find the length of the traces in Ints_A00_i00.hdf5 is 10 times the number of the interesting clock cycles for the first 32-bit word in state A00 as a result.  

5. Template profiling:

	>> cd template_profiling_bytes/
	>> ./script_all.sh

   This step is to build templates with multiple linear regression and linear discrimenant analysis (LDA). The resulting templates will be stored in "template_profiling_bytes/templateLDA_O010.zip"


