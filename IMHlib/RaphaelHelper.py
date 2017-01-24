
if __name__ == '__main__':
    import sys
    sys.path.append(sys.path[0].rstrip('IMHlib'))

import IMHlib	

print('''
                              Raphael Helper
      ''')

margin = IMHlib.Margin()

file = margin.FileSelect(['.xlsx','.xls'])
output_loc = margin.OutLoc(file)

flag = margin.ProcessFigure()

print('\n 正在处理中...')

from IMHlib.LayerMessage import LayerMessage


layermessage = LayerMessage(file)

from IMHlib.Writer import PreRun,Dicspts,TechChar

prerundata = PreRun(output_loc)
dicspts = Dicspts(output_loc)
techchar = TechChar(output_loc)

for base in ['AA','STI']:
    for corner in ['Typical','Fast','Slow']:
        DF = layermessage.Zmin(base,corner,flag)
        techchar.write(base,corner,DF)
        dicspts.write(base,corner,DF)
        prerundata.write(base,corner,DF)
    
print('\n 绘图中...')
from IMHlib.Ploter import CrossSection
try:
    crosssection = CrossSection(output_loc)
    crosssection.plot(layermessage.ExtractValue('Diel'),layermessage.Zmin('STI','Typical',flag))
except:
    print('\n 绘图错误，请查看 pre_run_datas.xls 有无异常数值。')






