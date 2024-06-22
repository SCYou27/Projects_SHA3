# Detection traces

Detection: the main goal of tasks in "0002_detection/" is to determine the points of interests (or interesting clock cycles).

1. Please download the raw traces used in this phase from the following website:

	https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0002_detection/

   Alternatively, just go to the directory "Raw/" to execute the script to download the raw traces:

	>> cd Raw/
	>> ./script_all.sh

2. Trace pre-processing:

	>> cd Code_preprocessing/
	>> ./script_all.sh

   This step will check the quality of the raw traces in this phase against the reference trace ("0001_referece/Code_reference/ref_trace.npy"), and also extract the I/O data in the archived raw trace ZIP files.

   The processed trace will be stored in an independent directory "0002_detection/Processed_HDF5/" as four HDF5 files, where each contains 4000 traces.

3. Intermeidate value calculation:

	>> cd Code_intermediate_values/
	>> ./script_all.sh

   Based on the extracted I/O data, this step is to calculate our target intermediate values and store them in bits (binary variables) for the multiple linear regression in the later detections.

4. R^2 values:

	>> cd Code_detection_R2/
	>> ./script_all.sh

   This step is to do multiple linear regression on the target intermediate values and the processed traces (one sample per clock cycle) to find the R^2 values for each target byte, and then add up the values from the four member bytes in a 32-bit word to find the summed R^2 values.

5. Determine the interesting clock cycles:

	>> cd Code_extract_ics/
	>> ./script_all.sh

   This step is to select the interesting clock cycles according to whether the summed R^2 value of a 32-bit word is higher than a given threshold. We used the ones with threshold equal to 0.010 in the later experiments, where the interesting clock cycle sets are stored in "Code_extract_ics/ics_original_010.zip"



