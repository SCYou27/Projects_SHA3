# Detection traces

The main goal of the tasks in "0002\_detection/" is to determine the points of interest (or interesting clock cycles).

1. Please download the raw traces used in this phase from the following website:

	https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0002_detection/

   Alternatively, go to the directory "Raw/" to execute the script to download the raw traces:

	`cd Raw/`  
	`./script_all.sh`  

2. Trace pre-processing:

	`cd Code_preprocessing/`  
	`./script_all.sh`  

   This step will check the quality of the raw traces in this phase against the reference trace ("../0001\_referece/Code\_reference/ref\_trace.npy"), and then extract the I/O data in the archived raw trace ZIP files.

   The processed trace will be stored in an independent directory "0002\_detection/Processed\_HDF5/" as four HDF5 files, each containing 4000 traces.

3. Intermeidate value calculation:

	`cd Code_intermediate_values/`  
	`./script_all.sh`  

   Based on the extracted I/O data, this step will calculate our target intermediate values and store them in bits (binary variables) for the multiple linear regression in the later detections.

4. Coefficient of determination (_R_<sup>2</sup>) values:

	`cd Code_detection_R2/`  
	`./script_all.sh`  

   This step is for multiple linear regression on the target intermediate values and the processed traces (one sample per clock cycle) to find the _R_<sup>2</sup> values for each target byte, and then add up the values from the four fragmented bytes in a 32-bit word to find the summed _R_<sup>2</sup> values.

5. Determine the interesting clock cycles:

	`cd Code_extract_ics/`  
	`./script_all.sh`  

   This step will select the interesting clock cycles according to whether the summed _R_<sup>2</sup> value of a 32-bit word is higher than a given threshold. We used the ones with a threshold equal to 0.010 in the later experiments, where the interesting clock cycle sets are stored in "Code\_extract\_ics/ics\_original\_010.zip"



