# Attack on the SHA3-512 hash function

The main goal of the tasks in "0006\_test\_SHA3-512/" is to perform a Soft Analytical Side-Channel Attack (SASCA) on the SHA3-512 hash function.

Hash functions support arbitrary-length inputs. Therefore, it may require more than one invocation of Keccak-_f_[1600] permutation to absorb the input. Here we further separate this data set into the following five subsets by the number of invocations required:

 - "SHA3\_512\_I01/": attack on 1000 executions of SHA3-512 with one invocation of Keccak permutation.
 - "SHA3\_512\_I02/": attack on 1000 executions of SHA3-512 with two invocations of Keccak permutation.
 - "SHA3\_512\_I04/": attack on 1000 executions of SHA3-512 with four invocations of Keccak permutation.
 - "SHA3\_512\_I05/": attack on 1000 executions of SHA3-512 with five invocations of Keccak permutation.
 - "SHA3\_512\_I10/": attack on 1000 executions of SHA3-512 with ten invocations of Keccak permutation.

Please check the README.md file in each sub-directory for more instructions.


