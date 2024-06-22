import numpy as np
import os
import Template_validate_LDA as template
import serv_manager as svm
import sys
L = int(sys.argv[1])
U = int(sys.argv[2])
for tSet in range(L, U):
  template.main(tSet)
  print("++++++++++++++++++++++++++++++++++++++++++++++++++")
