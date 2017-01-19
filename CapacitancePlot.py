#Version 1.1
import os,sys

print(' Waitting...')

def main(folder):

	aaTT	=	folder+'/'+'AA_TT.out'
	aaFF	=	folder+'/'+'AA_FF.out'
	aaSS	=	folder+'/'+'AA_SS.out'
	stiTT	=	folder+'/'+'STI_TT.out'
	stiFF	=	folder+'/'+'STI_FF.out'
	stiSS	=	folder+'/'+'STI_SS.out'

	def Capac(x):
		if x=='Ctotal':
			n		=	2
			title1	=	'Ctotal'
		elif x=='Cbottom':
			n		=	3
			title1	=	'Cbottom'
		elif x=='Ccoup':
			n		=	4
			title1	=	'Ccoup'
		elif x=='Cf':
			n		=	5
			title1	=	'Cf'
			
		def pltData(type,loc,n):
			
			dic2	= 	{'AA_TT':aaTT, 'AA_FF':aaFF, 'AA_SS':aaSS, 'STI_TT':stiTT, 'STI_FF':stiFF, 'STI_SS':stiSS}
			fpath	= 	dic2.get(type)
			m		= 	open(fpath,'r').readlines()
							
			pltData, tempx, tempy	=	[], [], []
			width	=	float(m[loc + 7].split(' ')[1])
					
			for k in range(spaceN):
				values	=	m[loc + 7 + k].split(' ')
						
				while '' in values:
					values.remove('')

				ct	=	list(map(float,values))
				tempx.append(ct[1]) 
				tempy.append(ct[n])
				pltData.append(width)
				pltData.append(tempx)
				pltData.append(tempy)					
			return pltData													# return style: [width,[spacing1,spacing2,..],[value1,value2,..]]
		
		def onefig(x):
			onefig	=	[]
			pltTT	=	pltData(x+'_TT',loc,n)
			pltFF	=	pltData(x+'_FF',loc,n)
			pltSS	=	pltData(x+'_SS',loc,n)
				
			if x=='STI':
				title3	=	name + '-FIELD_OXIDE\n'
				title	=	title1 + ' versus Spacing for ' + title3
			else:
				title	=	title1 + ' versus Spacing for ' + title2
			onefig	=	[pltTT, pltFF, pltSS, title]
			return onefig				
		
		overall_data = []
		#location=[]		
		c_AA_T	=	open(aaTT,'r').readlines()		
		for loc,line in enumerate(c_AA_T):
			if 'Generic Structure Name: arr_above_gp' in line:				# only concern the 1st structure (Pizza)
				#print('I find you!: %d' %loc)
				s	 =	c_AA_T[loc + 1].split(',')
				name =	c_AA_T[loc + 1].split(' ').pop().split(',')[0]
				if s[-1] == 'substrate\n': 									# define title				
					title2 = name + '-AA\n'
					signal = 1 												# only in this situation, get substrate data from STI datas
				else:
					title2 = name + '-' + s[-1]	
					signal = 0 												# do nothing
			
				#**************************************************
				# get the quantity of Spacing for one time only
				if c_AA_T[loc-8]=='---------------------------------------------------------------------------\n':
					spaceN=1
					while c_AA_T[loc+7+spaceN]!='\n':
						spaceN+=1
				#**************************************************
								
				if signal == 1:			
					overall_data.append(onefig('AA'))
					overall_data.append(onefig('STI'))	
				elif signal == 0:
					overall_data.append(onefig('AA'))
					
				#location.append(loc) 										# record the location							
		#print(location)	
		del c_AA_T
		return overall_data	
	#print(Capac('Ctotal'))
	
	import matplotlib.pyplot as plt
	from matplotlib.backends.backend_pdf import PdfPages
	
	for c in ['Ctotal','Cbottom','Ccoup','Cf']:
		all	=	Capac(c)
		pdf	=	PdfPages(folder + '/' + c + '.pdf')
		for i in range(len(all)): 											# total figure nums
			fig	=	plt.figure()
			all_seg	=	all[i]

			xT, xF, xS = all_seg[0][1], all_seg[1][1], all_seg[2][1]
			yT, yF, yS = all_seg[0][2], all_seg[1][2], all_seg[2][2]
			wT, wF, wS = all_seg[0][0], all_seg[1][0], all_seg[2][0]
			#print(yF)
			plt.xlim(-1,12)
			
			plt.plot(xS, yS, '-ro')
			plt.plot(xT, yT, '-o')
			plt.plot(xF, yF, '-go')
			
			plt.title(all_seg[3])
			plt.ylabel('Ctotal(fF)')
			plt.xlabel('Spacing(um)')
			plt.legend(('W-SS=' + str(wS), 'W-TT=' + str(wT), 'W-FF=' + str(wF)), loc='upper center')
			#plt.legend(('W-SS='+str(wS),'W-TT='+str(wT),'W-FF='+str(wF)),bbox_to_anchor=(0.,1.02,1.,1.02),loc=3,ncol=2,mode="expand",borderaxespad=0.)
			pdf.savefig(fig)
			plt.close(fig)
			print(' %s No.%d figures completed'%(c,i+1)) 	
		print('\n')
		pdf.close()
			
if __name__=='__main__':
	folder = sys.path[0]		
	main(folder)	