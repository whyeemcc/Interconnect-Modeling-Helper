import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Ploter:
	
	def __init__(self,output):
		self.output = output
	
	def CrossSection(self,DielLayer,DF):
		"""
		DielLayer is RawData extract from excel to polt AA
		DF is STI,TT DataFrame
		"""
		Diel,Cond = DF['Diel'],DF['Cond']
		# Create a figure
		fig	= plt.figure(figsize = (20,20))
		ax = fig.add_subplot(111, aspect = 'equal')
		# Define the size of figure
		length	= 1.5 * max(Cond['width']) 
		height	= sum(Diel['thick'])
		plt.xlim(-length/2, length/2)
		plt.ylim(0, height)
		# Define the axis of y list
		Dielyticks = [0]
		
		# Plot dielectric layer
		for name,value in Diel.iterrows():
			'''
			left-down point'x of rectangle
			left-down point'y of rectangle
			'''
			x	= -length/2							 
			y	= sum(Diel[:name]['thick']) - value['thick']
			thick = value['thick']
			ax.add_patch(patches.Rectangle((x,y), length, thick, fill = False))
			ax.annotate(name, xy=(0,0), xytext=(x+length/20, y+thick/2))
			Dielyticks.append(y + thick)
		
		# Plot AA
		x, y = -1/2*length/2, 0
		thick = (DielLayer['thick'][0] - DielLayer['thick'][1]) * 1e-4       		
		ax.add_patch(patches.Rectangle((x,y), 1/2*length, thick, facecolor = 'green'))
		ax.annotate(DielLayer.index[1], xy=(0,0), xytext=(-length/2+length/20, thick))
		Dielyticks.append(thick)
		
		# Plot conductor layer
		for name,value in Cond.iterrows():
			x	= -value['width']/2
			y	= value['Zmin']
			ax.add_patch(patches.Rectangle((x,y), value['width'], value['thick'], facecolor = 'red'))
			ax.annotate(name+' = '+'%.3f'%value['thick']+'um', xy=(0,0), xytext=(0, y+value['thick']/2))
		
		ax.set_yticks(Dielyticks)
		plt.title('Cross-section of interconnect(Typical)')
		plt.xlabel('Width(um)')
		plt.ylabel('Height(um)')
		
		fig.savefig(self.output+'/Cross-section of interconnect.png',dpi=200)
		print('\n 已完成:\t Cross-section figure')
		plt.show()
		
		# check if there is an error
		if Cond['Zmin'][-1]+Cond['thick'][-1] >= sum(Diel['thick']):
			print("\n Warnning: The top conductor's Zmax is bigger than top dielectric's Zmax.\n This is not allowed in Raphael! Please check.")
