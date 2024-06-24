# Template attacks on SHA-3 implementations

This repository contains two projects of template attacks on SHA-3 (Keccak) functions implemented on different devices.

1. project_SHA3-XMEGA: an 8-bit implementation of hash function SHA3-512 on a side-channel test board with an Atmel XMEGA 256 A3U microcontroller, designed by Marios Omar Choudary (https://www.cl.cam.ac.uk/~osc22/docs/efficient_templates.pdf). _The code of this project is still under review and is expected to be available before the end of July 2024._

2. project_SHA3-32bit: a 32-bit implementation of four SHA-3 hash functions (SHA3-512, SHA3-384, SHA3-256, SHA3-224) and two SHAKE extendable-output functions (SHAKE256, SHAKE128) on ChipWhisperer-Lite 32-bit board (https://rtfm.newae.com/Starter%20Kits/ChipWhisperer-Lite/#1-part-32-bit)

These codes and experiments are related to my PhD thesis and two peer-reviewed papers:

 -  Shih-Chun You:  
    _Single-trace template attacks on permutation-based cryptography_,  
    Apollo - University of Cambridge Repository,  
    PhD thesis, 2022, DOI: https://doi.org/10.17863/CAM.100592

 -  Shih-Chun You, Markus G. Kuhn:  
    _A template attack to reconstruct the input of SHA-3 on an 8-bit device_,  
    International Workshop on Constructive Side-Channel Analysis and Secure Design  
    (COSADE 2020), Pages 25-42, LNCS 12244,  
    DOI: https://doi.org/10.1007/978-3-030-68773-1_2  

 -  Shih-Chun You, Markus G. Kuhn:  
    _Single-trace fragment template attack on a 32-bit implementation of Keccak_,  
    CARDIS 2021, 11–12 November 2021, Lübeck, Springer, LNCS 13173, 2022,  
    DOI: "https://doi.org/10.1007/978-3-030-97348-3_1"
