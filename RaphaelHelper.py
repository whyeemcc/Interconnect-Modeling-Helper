
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

try:
	layermessage = LayerMessage(file)

	from IMHlib.Writer import Writer
	
	writer = Writer(output_loc)
	prerundata = writer.WritePreRun(output_loc)	
	for base in ['AA','STI']:
		for corner in ['Typical','Fast','Slow']:
			DF = layermessage.Zmin(base,corner,flag)
			writer.WriteTechChar(base,corner,DF)
			writer.WriteDics(base,corner,DF)
			prerundata.WriteBlock(base,corner,DF)
	prerundata.Save()
	print('\n 已完成:\t techChar.tch')
	print('\n 已完成:\t disc.pts')
	
except:
	print('\n Excel 文件提取信息出现错误，请参照教程再检查一遍。')
	exit()

from IMHlib.Ploter import Ploter

ploter = Ploter(output_loc)
ploter.CrossSection(layermessage.ExtractValue('Diel'),layermessage.Zmin('STI','Typical',flag))







