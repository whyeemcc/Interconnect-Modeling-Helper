
if __name__ == '__main__':
	import sys
	sys.path.append(sys.path[0].rstrip('IMHlib'))

import IMHlib	

print('''
                              Capacitance Extraction
	  ''')

margin = IMHlib.Margin()

folder = margin.FileSelect([''])








exit()




# Update Date:	2016.11.09
# Author:		Grothendieck
# Version:		2.1.1	:	Recover to the previous version
#				2.1.0	:	Remove the repetitive capcitance block(Conductor vs Conducotr in STI type).
#				2.0.0	:	Extract 'Structure-1.txt' & 'Structure-1.txt'.
#				1.0.0	:	Extract capacitances into a excel table.
import os,sys

def main(folder):

	aaTT	=	folder+'/'+'AA_TT.out'
	aaFF	=	folder+'/'+'AA_FF.out'
	aaSS	=	folder+'/'+'AA_SS.out'
	stiTT	=	folder+'/'+'STI_TT.out'
	stiFF	=	folder+'/'+'STI_FF.out'
	stiSS	=	folder+'/'+'STI_SS.out'

	def V(file):
		out	= open(file,'r')
		content = out.readlines()

		value_list = []
	
		for k,line in enumerate(content):
			if 'Generic Structure Name: arr_above_gp' in line: 					# only concern the the 1st structure (Pizza)
				if 'substrate\n' in content[k+1]: 								# only concern capacitance between conductors and substrate
					value = content[k+8].split(' ')
					while '' in value:
						value.remove('')
							
					name	= content[k + 1].split(' ').pop().split(',')[0] 	# get conductor name
					C_aera	= content[k + 3].split(' ').pop() 					# get Carea value
					Width	= content[k + 8].split(' ')[1] 						# get width value
					C_a		= float(C_aera)*float(Width)						# calculate Ca
						
					value.insert(4,str(C_a))
					value.insert(0,name)
					value.pop()
					value_list.append(value)
		return value_list
	
	#------------------------generate excel-----------------------------
	import xlwt
	excel=xlwt.Workbook(encoding='utf-8')
	table=excel.add_sheet('Interconnect Model',cell_overwrite_ok=True)
	#style
	alignment		= xlwt.Alignment()
	alignment.horz	= xlwt.Alignment.HORZ_CENTER
	alignment.vert	= xlwt.Alignment.VERT_CENTER

	borders			= xlwt.Borders()
	borders.left	= 1
	borders.right	= 1
	borders.top		= 1
	borders.bottom	= 1

	font1				= xlwt.Font()
	font1.name			= 'Arial'
	font1.colour_index	= 4              	# blue
	font2				= xlwt.Font()
	font2.name			= 'Arial'
	font2.colour_index	= 2              	# red

	patternTT			= xlwt.Pattern()
	patternTT.pattern	= 1
	xlwt.Pattern.SOLID_PATTERN 				# full fill
	patternTT.pattern_fore_colour	= 171 	# yellow

	patternFF			= xlwt.Pattern()
	patternFF.pattern	= 1
	xlwt.Pattern.SOLID_PATTERN 
	patternFF.pattern_fore_colour	= 178 	# green

	patternSS			= xlwt.Pattern()
	patternSS.pattern	= 1
	xlwt.Pattern.SOLID_PATTERN 
	patternSS.pattern_fore_colour	= 29  	# pink

	patternX1			= xlwt.Pattern()
	patternX1.pattern	= 1
	xlwt.Pattern.SOLID_PATTERN 
	patternX1.pattern_fore_colour	= 42 	# shallow green

	patternX2			= xlwt.Pattern()
	patternX2.pattern	= 1
	xlwt.Pattern.SOLID_PATTERN 
	patternX2.pattern_fore_colour	= 52 	# shallow pink

	style			=	xlwt.XFStyle() 
	style.alignment	=	alignment
	style.borders	=	borders
	style1			=	xlwt.XFStyle() 
	style1.alignment=	alignment
	style1.borders	=	borders
	style1.font		=	font1
	style2			=	xlwt.XFStyle()
	style2.alignment=	alignment
	style2.borders	=	borders
	style2.font		=	font2

	styleTT				=	xlwt.XFStyle()
	styleTT.alignment	=	alignment
	styleTT.borders		=	borders
	styleTT.pattern		=	patternTT

	styleFF				=	xlwt.XFStyle()
	styleFF.alignment	=	alignment
	styleFF.borders		=	borders
	styleFF.pattern		=	patternFF

	styleSS				=	xlwt.XFStyle()
	styleSS.alignment	=	alignment
	styleSS.borders		=	borders
	styleSS.pattern		=	patternSS

	styleX1				=	xlwt.XFStyle()
	styleX1.alignment	=	alignment
	styleX1.borders		=	borders
	styleX1.pattern		=	patternX1

	styleX2				=	xlwt.XFStyle()
	styleX2.alignment	=	alignment
	styleX2.borders		=	borders
	styleX2.pattern		=	patternX2


	def col(x):
		if len(x) == 1:
			col = ord(x) - ord('A')
		elif len(x) == 2:
			col	= 26 + ord(x[1]) - ord('A')
		return col
	
	#-----------------------------------------------------Generate excel----------------------------------------------------
	table.write(0, 0, '***********************')
	table.write(1, 0, '* Layers: On FOX *')
	table.write(2, 0, '***********************')
	table.write(0, col('F'), 'um/m', style)
	table.write(0, col('G'), 'fF/F', style)
	table.write(1, col('F'), 1.00E-06, style)
	table.write(1, col('G'), 1.00E-15, style)
	table.col(1).width = 256*20
	title1=['','','Width','Spacing','Ctotal','Cbottom','Ca','Ccoup','Cf']
	title2=['Cf_total','Caera','Caera','Ccoup','Cf','Cf_total']
	title3=['','Layers','um','um','fF/um','fF/um','fF/um','fF/um','fF/um','fF/um','fF/um^2','F/m^2','F/m','F/m','F/m']
	
	
	#--------------------------------------1st table-----------------------------------
	for k,line in enumerate(title1):
		table.write(3, k, line, style1)

	for k,line in enumerate(title2):
		if k == 1 or k == 2:
			continue
		table.write(3, col('J')+k, line, style2)
	table.write_merge(3, 3, col('K'), col('L'),'Caera', style2)

	for k,line in enumerate(title3):
		table.write(4, k, line, style)		
		
	styles=[styleTT,styleFF,styleSS]
	for i,corner in enumerate([stiTT, stiFF, stiSS]):											# only extract STI type
		result 	=	V(corner)
		layer 	=	len(result)
		table.write(5 + i*layer, 0, ['TT','FF','SS'][i], styles[i])
		table.write_merge((5+i*layer) + 1, (5+i*layer) + (layer-1), 0, 0, '', style) 			# blank

		for n,line in enumerate(result):
			row	= 5 + i * layer + n

			for k,value in enumerate(line):
				if k == 0: 																		# layer name
					table.write(row, 1 + k, value, styles[i])
				else: 																			# float numbers
					table.write(row, 1 + k, format(eval(value),'.2E'), styles[i])

			table.write(row,col('J'), xlwt.Formula('H'+str(row+1)+'+'+'I'+str(row+1)),styles[i])
			table.write(row,col('K'), xlwt.Formula('G'+str(row+1)+'/'+'C'+str(row+1)),styles[i])
			table.write(row,col('L'), xlwt.Formula('K'+str(row+1)+'*G2/F2/F2'),styles[i])
			table.write(row,col('M'), xlwt.Formula('H'+str(row+1)+'*G2/F2'),styles[i])
			table.write(row,col('N'), xlwt.Formula('I'+str(row+1)+'*G2/F2'),styles[i])
			table.write(row,col('O'), xlwt.Formula('J'+str(row+1)+'*G2/F2'),styles[i])
			
	#--------------------------------------2nd table---------------------------------------
	table.write_merge(2, 2, col('R'), col('S'), 'Interconnect_TT', style2)
	table.write_merge(2, 2, col('T'), col('U'), 'Interconnect_FF', style2)
	table.write_merge(2, 2, col('V'), col('W'), 'Interconnect_SS', style2)
	table.write_merge(3, 3, col('R'), col('S'), 'TT', style2)
	table.write_merge(3, 3, col('T'), col('U'), 'SRFC', style2)
	table.write_merge(3, 3, col('V'), col('W'), 'FRSC', style2)
	table.write_merge(3, 3, col('X'), col('Y'), 'SRFC-TT', style2)
	table.write_merge(3, 3, col('Z'), col('AA'),'FRSC-TT', style2)
	title4=['Cond.-FOX','COX','CFOX','COX','CFOX','COX','CFOX','DCOX','CFOX','DCOX','CFOX']

	for k,line in enumerate(title4):
		table.write(4, col('Q') + k, line, style2)
		
	table.col(col('Q')).width=256*15		
	for row in range(5,5+layer):
		table.write(row, col('Q'), xlwt.Formula('B'+str(row+1)), style) 						# Cond.-FOX
		
		table.write(row, col('R'), xlwt.Formula('L'+str(row+1)), styleTT) 						# TT COX
		table.write(row, col('S'), xlwt.Formula('N'+str(row+1)), styleTT) 						# TT FCOX
		
		table.write(row, col('T'), xlwt.Formula('L'+str(row+1+layer)), styleFF) 				# SRFC COX
		table.write(row, col('U'), xlwt.Formula('N'+str(row+1+layer)), styleFF) 				# SRFC FCOX
		table.write(row, col('V'), xlwt.Formula('L'+str(row+1+layer*2)), styleSS) 				# FRSC COX
		table.write(row, col('W'), xlwt.Formula('N'+str(row+1+layer*2)), styleSS) 				# FRSC FCOX
		
		table.write(row, col('X'), xlwt.Formula('T'+str(row+1)+'-'+'R'+str(row+1)), styleX1) 	# SRFC-TT DCOX
		table.write(row, col('Y'), xlwt.Formula('U'+str(row+1)+'-'+'S'+str(row+1)), styleX1) 	# SRFC-TT CFOX
		table.write(row, col('Z'), xlwt.Formula('V'+str(row+1)+'-'+'R'+str(row+1)), styleX2) 	# FRSC-TT DCOX
		table.write(row, col('AA'), xlwt.Formula('W'+str(row+1)+'-'+'S'+str(row+1)), styleX2) 	# FRSC-TT CFOX
			
	excel.save(folder+'/'+'Capacitance Extraction.xls')
	print('\n Completed:\t Excel Done!')
	

	#-------------------------------------------Interconnect Capacitance Table--------------------------------------------------
	import time
	date = time.strftime("%Y-%m-%d",time.localtime(time.time()))

	def Modeltxt(struc):
					
		#----------------------------------------Core function: Block Generator-------------------------------------------------				
		def writeblock(struc, AcStName):
			if struc == 'arr_above_gp':
				f.write('''
*************************
* Layers:\t %s
*************************'''%(AcStName))
				f.write('''
Width	Spacing	Ctotal	Cbottom	Ca	Ccoup	Cf
(um)	(um)	(fF/um)	(fF/um)	(fF/um)	(fF/um)	(fF/um)
------	-------	--------	--------	--------	--------	--------\n''')
				next	= 7																		# 7 rows below 'arr_btwn_gps' is data						
				C_aera 	= content[ k + 3 ].split(' ').pop()  
				Width	= content[ k + next ].split(' ')[1]

				spaceN = 1
				while content[k + next + spaceN] != '\n':
					spaceN += 1	
							
				for i in range(spaceN):	
					list = content[k + next + i].split(' ')
					while '' in list:
						list.remove('')
								
					C_a = float(C_aera)*float(Width)
								
					list.insert(4,str(C_a))
					list.pop()							
									
					for j,num in enumerate(list):
						if j in [0,1]:
							f.write('%.3f'% (eval(num)) + '\t')
						else:
							f.write(format(eval(num),'.2E') + '\t')
					f.write('\n')
				f.write('------	-------	--------	--------	--------	--------	--------\n')
							
			elif struc == 'arr_btwn_gps':
				f.write('''
*************************
* Layers:\t %s
*************************'''%(AcStName))
				f.write('''
Width	Spacing	Ctotal	Cbottom	Ctop	Cb_area	Ct_area	Ccoup	Csd	Csu
(um)	(um)	(fF/um)	(fF/um)	(fF/um)	(fF/um)	(fF/um)	(fF/um)	(fF/um)	(fF/um)
-------	-------	--------	--------	--------	--------	--------	--------	--------	--------\n''')

				next		= 8																	# 8 rows below 'arr_btwn_gps' is data
				C_aera_bot 	= content[k + 3].split(' ').pop()  
				C_aera_top	= content[k + 4].split(' ').pop()
				Width	= content[k + next].split(' ')[1]
							
				spaceN = 1
				while content[k + next + spaceN] != '\n':
					spaceN += 1							
								
				for i in range(spaceN):	
					list = content[k + next + i].split(' ')
					while '' in list:
						list.remove('')
						
					Cb_area = float(C_aera_bot) * float(Width)
					Ct_area = float(C_aera_top) * float(Width)
							
					list.insert(5, str(Cb_area))
					list.insert(6, str(Ct_area))
					list.pop()							
									
					for j,num in enumerate(list):
						if j in [0,1]:                                # width & spacing don't need any format
							f.write('%.3f'% (eval(num)) + '\t')
						else:
							f.write(format(eval(num),'.2E') + '\t')
					f.write('\n')
				f.write('-------	-------	--------	--------	--------	--------	--------	--------	--------	--------\n')
		#------------------------------------------------------------------------------------------------------------------------------------
								
		if struc == 'arr_above_gp':
			fname	= 'Structure-1'
			suffix	= '(Parallel lines above a bottom plate)'
		elif struc == 'arr_btwn_gps':
			fname	= 'Structure-2'
			suffix	= '(Parallel lines above a bottom plate)'
		f = open(folder + '/' + fname + '.txt','w')			
		
		dic = {'AATT':aaTT, 'AAFF':aaFF, 'AASS':aaSS, 'STITT':stiTT, 'STIFF':stiFF, 'STISS':stiSS}
		for co in ['TT','FF','SS']:
			f.write('''
***********************************************************************
*****           Interconnect Capacitance Table             ************
***********************************************************************
			
Process:\t 请搜索全部替换例如："0.18um 1P6M Logic Salicide, Dual Voltage (1.8V/3.3V)"
Version:\t 请搜索全部替换例如：0.3
Date:\t %s
Corner:\t %s
Structure:\t%s
(Please refer to SPICE model document for the definition of each capacitance)\n
			'''%(date, co, fname+suffix))
			
			# extract all Actual Structure: AA 		
			content = open(dic['AA'+co],'r').readlines()
			for k,line in enumerate(content):
				if struc in line:						
					
					if struc == 'arr_above_gp':																					
						up 			= 	content[k + 1].split(' ').pop().split(',')[0]
					elif struc == 'arr_btwn_gps':							
						upgather 	= 	content[k + 1].split(' ').pop().split(',')
						up 			=	upgather[0] + '-' + upgather[1]
						
					down	=	content[k + 1].split(' ').pop().split(',')[-1][:-1]						
					if down == 'substrate':
						down	= 	'AA *'
					else: down	= 	down + ' *'
					
					AcStName = up + '-' + down
																			
					writeblock(struc, AcStName)
					
			# extract all Actual Structure: FIELD_OXIDE 
			content = open(dic['STI'+co],'r').readlines()
			for k,line in enumerate(content):
				if struc in line:
											
					if struc == 'arr_above_gp':
						up 			= 	content[k+1].split(' ').pop().split(',')[0]
					elif struc == 'arr_btwn_gps':
						upgather 	= 	content[k+1].split(' ').pop().split(',')
						up 			= 	upgather[0] + '-' + upgather[1]
						
					down	=	content[k + 1].split(' ').pop().split(',')[-1][:-1]	
					if down == 'substrate':
						down = 'FIELD_OXIDE *'
					else: down = down + ' *'
					
					AcStName = up + '-' + down
					
					writeblock(struc, AcStName)
		f.close()

	Modeltxt('arr_above_gp')
	print('\n Completed:\t Structure-1.txt')

	Modeltxt('arr_btwn_gps')
	print('\n Completed:\t Structure-2.txt')
		
if __name__=='__main__':
	folder = sys.path[0]		
	main(folder)	


