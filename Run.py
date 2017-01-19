import os
import sys

path = sys.path[0]
lib = '/IMHlib'

server_dir = r'\\tddevice\Compact Modeling & PDK\TBDE\CompactModel2\NHD_Model2\tools\Interconnect Modelling Helper'
RunOnServer = '\\tddevice' in path
AlreadyExist = os.path.exists(path+lib)
NoneExist = not AlreadyExist

if RunOnServer: print(' Do not run me in server! Please run me in local disk.')

elif NoneExist: 
	import shutil
	ans = input(" You don't have a Interconnect Modelling Helper.\n Do you want to download it? y or n ?\n\n Your answer is : ")	
	if ans in ['y','Y']:
		print(' Downloading... wait a few second')
		try:
			shutil.copytree(server_dir+lib,path+lib)
		except IOError:
			print('\n\n Oh! The Lib files on server are missing, please contact the maintenance personnel.');exit()
		print(' Download successfully')
	else: exit()

if AlreadyExist:
	import IMHlib
	import re
	ver_loc = IMHlib.__UPDATE_DATE__
	ver_ser = re.search("__UPDATE_DATE__ = '(.*)'",open(server_dir+'/IMHlib/__init__.py','r').read()).groups()[0]	

	try:	
		if ver_loc < ver_ser:
			import shutil
			#shutil.copytree(server_dir+lib,path+lib)
			print(' ******************\n Update finished \n ******************')
		else: print(' ******************\n No need to update \n ******************')
	except: print(" Oh! Can't check update, please contact maintenance personnel.")	

import IMHlib
print('''
                         INTERCONNECT MODELLING HELPER
						 
 Choose a tool you want to use:
 
 1 > Raphael Helper
 2 > Capacitance Extraction
 3 > Model QA
''')

margin = IMHlib.Margin()
ans = margin.Choice(['1','2','3'])

if ans == '1': import IMHlib.RaphaelHelper
elif ans == '2': import IMHlib.CapacitanceExtraction
elif ans == '3': import IMHlib.ModelQA