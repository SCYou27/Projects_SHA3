import numpy as np
import os
def Draw(bound, rd):
  Dir = "ics_original_"+bound+"/" 
  Outputs = "\\begin{table}\n"
  B_str = str(0.001*float(bound))
  Outputs += "\\caption{Numbers of detected interesting clock cycles in round "+str(rd)
  Outputs += " with threshold "+B_str+" ($\Omega = "+str(rd)+", R^2>"+B_str+"$)}\\"
  Outputs += "label{tab:ICS_O"+bound+"_R"+str(rd)+"}\n"
  Outputs += "\\begin{center}"
  Outputs += "\\begin{tabular}{|c|*{4}{c|}}\n\\hline\n"
  Outputs += "\\multirow{2}{*}{Lane[i]} & \n"
  Outputs += "\\multicolumn{2}{c|}{$\\mathbf{C}_{"+str(rd)+"}$} & \n"
  Outputs += "\\multicolumn{2}{c|}{$\\mathbf{D}_{"+str(rd)+"}$}\\\\\n\\cline{2-5}\n"
  Outputs += " & first 32 bits & second 32 bits & first 32 bits & second 32 bits\\\\\n\\hline\n"
  for i in range(0, 5):
    Outputs += ("["+str(i)+"]")
    Outputs += (" & "+str(len(np.load(Dir+"ics_C"+str(rd).zfill(2)+"_i"+str((2*i  )).zfill(2)+".npy"))))
    Outputs += (" & "+str(len(np.load(Dir+"ics_C"+str(rd).zfill(2)+"_i"+str((2*i+1)).zfill(2)+".npy"))))
    Outputs += (" & "+str(len(np.load(Dir+"ics_D"+str(rd).zfill(2)+"_i"+str((2*i  )).zfill(2)+".npy"))))
    Outputs += (" & "+str(len(np.load(Dir+"ics_D"+str(rd).zfill(2)+"_i"+str((2*i+1)).zfill(2)+".npy"))))
    Outputs += ("\\\\\n\\hline\n")
  Outputs += ("\\hline\n")
  Outputs += "\\multirow{2}{*}{Lane[i, j]} & \n"
  Outputs += "\\multicolumn{2}{c|}{$\\alpha'_{"+str(rd)+"}$} & \n"
  Outputs += "\\multicolumn{2}{c|}{$\\beta_{"+str(rd)+"}$}\\\\\n\\cline{2-5}\n"
  Outputs += " & first 32 bits & second 32 bits & first 32 bits & second 32 bits\\\\\n\\hline\n"
  for j in range(0, 5):
    for i in range(0, 5):
      Outputs += ("["+str(i)+", "+str(j)+"]")
      x = i+5*j
      Outputs += (" & "+str(len(np.load(Dir+"ics_A"+str(rd).zfill(2)+"_i"+str((2*x  )).zfill(2)+".npy"))))
      Outputs += (" & "+str(len(np.load(Dir+"ics_A"+str(rd).zfill(2)+"_i"+str((2*x+1)).zfill(2)+".npy"))))
      Outputs += (" & "+str(len(np.load(Dir+"ics_B"+str(rd).zfill(2)+"_i"+str((2*x  )).zfill(2)+".npy"))))
      Outputs += (" & "+str(len(np.load(Dir+"ics_B"+str(rd).zfill(2)+"_i"+str((2*x+1)).zfill(2)+".npy"))))
      Outputs += ("\\\\\n\\hline\n")
  Outputs += "\\end{tabular}\n"
  Outputs += "\\end{center}\n\\end{table}\n"
  print(Outputs)
  fileobj = open(("Tables/Table_"+bound+"_r"+str(rd).zfill(2)+".txt"), 'w')
  fileobj.write(Outputs)
  fileobj.close()
  return

if __name__=='__main__':
  for s in range(1, 10):
    tag = str(s*10).zfill(3)
    os.system(('unzip -qq ics_original_'+tag+'.zip'))
    for rd in range(0, 4):
      Draw(tag, rd)
    os.system(('rm -r ics_original_'+tag+'/'))
