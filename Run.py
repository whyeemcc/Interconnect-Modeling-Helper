import os
import sys

path = sys.path[0]
lib = '/IMHlib'

server_dir = r'\\tddevice\Compact Modeling & PDK\TBDE\CompactModel2\NHD_Model2\tools\Interconnect Modeling Helper'
RunOnServer = '\\tddevice' in path
AlreadyExist = os.path.exists(path+lib)
NoneExist = not AlreadyExist

if RunOnServer: input('\n 请将此文件夹拷贝至本地，再运行。');exit()

elif NoneExist: 
    import shutil
    ans = input("\n 检测到你还没有 Interconnect Modeling Helper.\n\n 是否现在下载？ y or n ?\n\n Your answer is : ")	
    if ans in ['y','Y']:
        print(' Downloading... wait a few second')
        try:
            shutil.copytree(server_dir+lib,path+lib)
            print(' Download successfully')
            AlreadyExist = True
        except IOError:
            input('\n\n Oh! 远程服务器端的文件不见了，请联系此tool的维护人员。'); exit()     
    else: exit()

if AlreadyExist:
    import IMHlib
    import re
    try:
        ver_loc = IMHlib.__UPDATE_DATE__
        ver_ser = re.search("__UPDATE_DATE__ = '(.*)'",open(server_dir+'/IMHlib/__init__.py','r').read()).groups()[0]	
        if ver_loc < ver_ser:
            import shutil
            shutil.rmtree(path+lib)
            shutil.copytree(server_dir+lib,path+lib)
            print(' ******************\n Update finished \n ******************')
        else: print(' ******************\n No need to update \n ******************')
    except:
        print("\n Oh! 无法检查更新，请联系此tool的维护人员。")	

print('''
                         INTERCONNECT MODELING HELPER

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

input('\n press any key to exit.')