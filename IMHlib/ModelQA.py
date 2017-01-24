if __name__ == '__main__':
    import sys
    sys.path.append(sys.path[0].rstrip('IMHlib'))

import IMHlib

margin = IMHlib.Margin()

folder = margin.FileSelect([''])

print('\n 绘图中...\n')

from IMHlib.Ploter import QA
QA = QA(folder)

from IMHlib.Extractor import QAC
QAC = QAC(folder)

for type in ['Ctotal','Cbottom','Ccoup','Cf']:
    all = QAC.extract(type)
    QA.plot(type,all)