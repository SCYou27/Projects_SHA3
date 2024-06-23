# Belief propagation testing

The main goal of tasks in "0005_SASCA/" is to test the factor graphs for belief propagation within a single Keccak-f[1600] permutation, which is associated with Fig. 4. in our paper. We did not record additional traces but just use the first 1000 in the validation set ("0004_validation/") for this phase.

1. Find answer bits for two states:

	`cd get_answers/`  
	`./script_all.sh`  

   This task extracts the answer bits for the input state and intermediate state A00 from the 1000 validation traces. We need the former to generate probability tables for the input capacity part and the latter to check if the belief propagation procedure stablizes and converges to the correct bit values.

2. Trace pre-processing:

	`cd Code_preprocessing/`  
	`./script_all.sh`  

   This step will check the quality of the raw traces in this phase against the reference trace ("0001_referece/Code_reference/ref_trace.npy"), and then extract the I/O data in the archived raw trace ZIP files.

   The processed trace will be stored in an independent directory "0004_validation/Processed_HDF5/" as four HDF5 files, where each contains 1000 traces.

3. Intermeidate value calculation:

	`cd Code_intermediate_values/`  
	`./script_all.sh`  

   Based on the extracted I/O data, this step will calculate our target intermediate values and store them in bytes as the answers for the quality evaluation.

4. Template validation:

	`cd template_validation_bytes/`  
	`./script_all.sh`  

   This step is to evaluate the quality of templates by providing a success rate and guessing entropy. The results will be stored in "template_validation_bytes/Result_Tables.zip"

   You can compare the numbers in Tables 2, 3, 4, and 5 in our paper with the following files:

   - Result_Tables/SR_table_A00_G0.txt
   - Result_Tables/GE_table_A00_G0.txt
   - Result_Tables/SR_table_B00_G0.txt
   - Result_Tables/GE_table_B00_G0.txt
   - Result_Tables/SR_table_C00_G0.txt
   - Result_Tables/GE_table_C00_G0.txt
   - Result_Tables/SR_table_D00_G0.txt
   - Result_Tables/GE_table_D00_G0.txt
