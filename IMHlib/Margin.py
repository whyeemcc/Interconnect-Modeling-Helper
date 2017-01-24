import os
import sys

class Margin:

    def __init__(self):
        self.path = sys.path[0]
        self.filelist = os.listdir(self.path)

    def Choice(self,depository):
        ans = input('\n select : ')
        while ans not in depository:
            ans = input(' Please re-select : ')
        return ans

    def ProcessFigure(self):
        print('''
       _____          _____                         _____          _____
            |________|                                   |________|
  Alpad_____|________|_____                    Alpad_____|________|_____	
                                                          ________
       ____________________                    M3   _____|________|_____
  M3        |________|                                    
                                                          ________
       ____________________                    M2   _____|________|_____
  M2        |________|
                                                          ________
       ____________________                    M1   _____|________|_____
  M1        |________|
  
             ________                                     ________  
  Poly   ___|--------|___                      Poly   ___|--------|___	
        |       AA       |  STI                      |       AA       |  STI
   _____|                |_____                 _____|                |_____    
 ********************************             ********************************
           1 : Cu Process                               2 : Al Process
        ''')

        ans=input(' 请选择一种制程。1（铜）or 2（铝） : ')
        while ans not in ['1','2']:
            ans = input(' please re-select : ')
        flag = {'1':1,'2':0}[ans]
        return flag

    def OutLoc(self,file):
        """
        file = 'X:\28hk.xlsx'
        outloc = 'X:\output__28hk'
        """
        OutLoc = self.path + '/output__' + os.path.splitext(os.path.split(file)[1])[0]
        if os.path.exists(OutLoc):
            pass
        else:
            os.mkdir(OutLoc)
        return OutLoc

    def FilesShow(self,list):
        '''
        Show the files under the current folder
        '''	
        for i,f in enumerate(list):
            print(' ',i+1,'>',f)

    def Suffix(self,name):
        return os.path.splitext(name)[-1]

    def FileSelect(self,dot):
        '''
        Confirm the selected file or folder is correct
        '''
        list = [x for x in self.filelist if self.Suffix(x) in dot]
        if dot == ['']:
            list.remove('IMHlib')
            print('\n 请选择包含 Raphael 计算结果的文件夹：\n')
        else: print('\n 请选择要处理的 Excel 文件：\n')
        self.FilesShow(list)
        dic = {str(i+1):f for i,f in enumerate(list)}
        return self.path + '/' + dic[self.Choice(dic)]
        