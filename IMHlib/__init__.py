__VERSION__ = '2.0.0'
__UPDATE_DATE__ = '2017.01.20'
__AUTHOR__ = 'Grothendieck'
'''
<Raphael Helper>:
Version:        2.0.0   :   Split the script to modules. Optimize the precision.
                1.1.0   :   Plot cross-section figure of TT corner.
                1.0.0   :   Generate pre_run_datas.xls & techar.tch & disc.pts files.

<Capacitance Extraction>:
Version:        2.0.0   :   Split the script to modules. Optimize the capcitance table and 'Structure.txt'
                1.1.2   :   Recover to the previous version
                1.1.1   :   Remove the repetitive capcitance block(Conductor vs Conducotr in STI type).
                1.1.0   :   Extract 'Structure-1.txt' & 'Structure-1.txt'.
                1.0.0   :   Extract capacitances into a excel table.
   
<Model QA>:
Version:        2.0.0   :   Split the script to modules.
                1.0.0   :   Extract the Cbottom/Ccoup/Cf/Ctotal to pdfs.
'''

from .Margin import Margin
