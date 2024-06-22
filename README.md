# Project_SHA3
The SHA3-32bit dataset contains recordings of the power-supply current changes of the 32-bit processor STM32F303RCT7, which has one ARM Cortex-M4 core, on a ChipWhisperer-Lite (CW-Lite) board.
We used an NI PXIe-5160 10-bit oscilloscope, which can sample at 2.5 GS/s into 2 GB of sampling memory, and an NI PXIe-5423 wave generator, as an external clock signal source, to supply the target board with a 5 MHz square wave signal.

More details of the attack are described in the following paper:

Shih-Chun You, Markus G. Kuhn:
Single-trace fragment template attack on a 32-bit implementation of Keccak
CARDIS 2021, 11–12 November 2021, Lübeck, Springer, LNCS 13173, 2022. DOI: "https://doi.org/10.1007/978-3-030-97348-3_1"

This project include all the code we used for the experiments. We suggest you have an access to a linux server with at least 2 TB storage to run the experiments.


We separated our project into the following phases:

1. Reference: the main goal of tasks in "0001_reference/" is to generate a reference trace (ref_trace.npy) for the trace quality control in the next phases.

2. Detection: the main goal of tasks in "0002_detection/" is to determine the points of interests (or interesting clock cycles).

3. Profiling (Training): the main goal of tasks in "0003_training/" is to build the templates used in our attacks.

4. Validation: the main goal of tasks in "0004_validation/" is to evaluate the quality of our templates by metrics of first-order success rate and guessing entropy.

(FOR TESTING)

5. Attacks: (code and data under review...)


