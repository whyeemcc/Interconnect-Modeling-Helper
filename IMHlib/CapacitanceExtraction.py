
if __name__ == '__main__':
    import sys
    sys.path.append(sys.path[0].rstrip('IMHlib'))

import IMHlib	

print('''
                              Capacitance Extraction
      ''')

margin = IMHlib.Margin()

folder = margin.FileSelect([''])

from IMHlib.Extractor import ParasticC,BlockC

parasticC = ParasticC(folder)

from IMHlib.Exporter import ParasticCxls,Structure
parasticCxls = ParasticCxls(folder)
Structure = Structure(folder)

DF = {}
for corner in ['TT','FF','SS']:
    DF[corner] = parasticC.extract('STI',corner)
parasticCxls.export(DF)    

for struc in ['Structure-1','Structure-2']:
    Structure.export(struc)