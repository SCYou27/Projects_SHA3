# Template attack on a 32-bit implementation of SHA-3 functions

The SHA3-32bit dataset contains recordings of the power-supply current changes of the 32-bit processor STM32F303RCT7, which has one ARM Cortex-M4 core, on a ChipWhisperer-Lite (CW-Lite) board.
We used an NI PXIe-5160 10-bit oscilloscope, which can sample at 2.5 GS/s into 2 GB of sampling memory, and an NI PXIe-5423 wave generator, as an external clock signal source, to supply the target board with a 5 MHz square wave signal.

More details of the attack are described in the following paper:

 - Shih-Chun You, Markus G. Kuhn:  
   _Single-trace fragment template attack on a 32-bit implementation of Keccak_  
   CARDIS 2021, 11–12 November 2021, Lübeck, Springer, LNCS 13173, 2022,  
   [DOI: 10.1007/978-3-030-97348-3\_1](https://doi.org/10.1007/978-3-030-97348-3_1)  

This project includes all the code we used for the experiments. We suggest you have access to a Linux server with at least 2 TB of storage to run the experiments.

Note that this is a newly optimized implementation for our experiments, and the numbers of results are slightly different from those published in our paper, but the differences are not statistically meaningful.

We divided our project into the following phases:

1. **Reference:** the main goal of tasks in "0001\_reference/" is to generate a reference trace (ref\_trace.npy) for trace quality control in the next phases.

2. **Detection:** the main goal of tasks in "0002\_detection/" is to determine the points of interest (or interesting clock cycles).

3. **Profiling (Training):** the main goal of tasks in "0003\_training/" is to build the templates used in our attacks.

4. **Validation:** the main goal of tasks in "0004\_validation/" is to evaluate the quality of our templates by metrics of first-order success rate and guessing entropy.

5. **Belief propagation testing:** the main goal of tasks in "0005\_SASCA/" is to test the factor graphs for belief propagation within a single Keccak-f[1600] permutation, which is associated with Fig. 4. in our paper.

6. **Attacks:** we separated the code and data of attacks by their target functions.
   - 0006\_SHA3-512/
   - 0007\_SHA3-384/
   - 0008\_SHA3-256/
   - 0009\_SHA3-224/
   - 0010\_SHAKE256/
   - 0011\_SHAKE128/

For every single small task in this project, we provide an all-in-one shell script to finish the tasks (script\_all.sh) and a restart script to clean all the generated data (clean.sh), please find the README.md file under each set for more instructions.
