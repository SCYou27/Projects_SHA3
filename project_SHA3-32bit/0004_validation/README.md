# Validation traces

The main goal of the tasks in "0004\_validation/" is to evaluate the quality of our templates by metrics of first-order success rate and guessing entropy.

1. Please download the raw traces used in this phase from the following website:

	https://www.cl.cam.ac.uk/research/security/datasets/sha3-32bit/Data/0004_validation/

   Alternatively, go to the directory "Raw/" to execute the script to download the raw traces:

	`cd Raw/`  
	`./script_all.sh`  

2. Trace pre-processing:

	`cd Code_preprocessing/`  
	`./script_all.sh`  

   This step will check the quality of the raw traces in this phase against the reference trace ("../0001\_referece/Code\_reference/ref\_trace.npy"), and then extract the I/O data in the archived raw trace ZIP files.

   The processed trace will be stored in an independent directory "0004\_validation/Processed\_HDF5/" as four HDF5 files, where each contains 1000 traces.

3. Intermeidate value calculation:

	`cd Code_intermediate_values/`  
	`./script_all.sh`  

   Based on the extracted I/O data, this step will calculate our target intermediate values and store them in bytes as the answers for the quality evaluation.

4. Template validation:

	`cd template_validation_bytes/`  
	`./script_all.sh`  

   This step will evaluate the quality of templates by providing a success rate and guessing entropy. The results will be stored in "template_validation_bytes/Result_Tables.zip"

   You can compare the numbers in Tables 2, 3, 4, and 5 in our paper with the following files:

   - Result\_Tables/SR\_table\_A00_G0.txt
   - Result\_Tables/GE\_table\_A00_G0.txt
   - Result\_Tables/SR\_table\_B00_G0.txt
   - Result\_Tables/GE\_table\_B00_G0.txt
   - Result\_Tables/SR\_table\_C00_G0.txt
   - Result\_Tables/GE\_table\_C00_G0.txt
   - Result\_Tables/SR\_table\_D00_G0.txt
   - Result\_Tables/GE\_table\_D00_G0.txt
