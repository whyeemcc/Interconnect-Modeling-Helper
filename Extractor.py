

class Extractor:
	
	def __init__(self,folder):
		self.AATT = folder + '/AA_TT.out'
		self.AAFF =	folder + '/AA_FF.out'
		self.AASS =	folder + '/AA_SS.out'
		self.STITT = folder + '/STI_TT.out'
		self.STIFF = folder + '/STI_FF.out'
		self.STISS = folder + '/STI_SS.out'

	def ParasticC(self):
		"""
		Parastic capacitance should be considered in 3T resistor model.
		Only concern the pizza type(arr_above_gp).
		Only concern the capacitance between conductor and substrate(XXX,above,substrate).
		"""
		import pandas as pd
		file = self.AAFF
		columns = ['Width','Spacing','Ctotal','Cbottom','Ca','Ccoup','Cf']
		content	= open(file,'r').readlines()

		conductor,valuelist = [],[]
		for k,line in enumerate(content):
			dic = {}
			if 'Generic Structure Name: arr_above_gp' in line: 					
				if 'above,substrate' in content[k+1]:
					# 8 lines under 'arr_above_gp' is the value what we want
					value = content[k+8].split(' ')
					while '' in value:
						value.remove('')
					# get conductor name		
					conductor.append(content[k+1].split(' ').pop().split(',')[0])
					# transfrom Ca (fF/um^2) to (fF/um)
					C_aera	= content[k+3].split(' ').pop()
					Width= content[k+8].split(' ')[1]
					dic['Ca'] = float(C_aera)*float(Width)
					
					for i,x in enumerate(['Width','Spacing','Ctotal','Cbottom','Ccoup','Cf']):
						dic[x] = eval(value[i])
					valuelist.append(dic)

		return pd.DataFrame(valuelist,index=conductor,columns=columns)


if __name__ == '__main__':
	import os,sys
	folder = sys.path[0]+'/test'
	result = Extractor(folder)
	print(result.ParasticC())