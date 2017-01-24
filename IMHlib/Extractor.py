'''
{*pizza type* Data Structure:}

Generic Structure Name: arr_above_gp
Actual Structure Name: Poly,above,substrate

C area:  3.83681e+00

    Width       Spacing      Ctotal       Cbottom      Ccoupli    Cperimeter     Lateral
 -----------  -----------  -----------  -----------  -----------  -----------  -----------
 1.80000e-01  2.57000e-01  9.84636e-01  9.22233e-01  3.12014e-02  1.15803e-01  8.01877e-03
 1.80000e-01  2.85000e-01  9.81217e-01  9.26295e-01  2.74610e-02  1.17834e-01  7.82638e-03
 1.80000e-01  3.10000e-01  9.79604e-01  9.30151e-01  2.47267e-02  1.19762e-01  7.66529e-03


{*sandwitch type* Data Structure:}
 
Generic Structure Name: arr_btwn_gps
Actual Structure Name: M3,Poly,substrate

C area to bottom:  3.83681e+00
C area to top:  3.69847e-02

    Width       Spacing      Ctotal       Cbottom       Ctop        Ccoupli        Csd          Csu        Lateral
 -----------  -----------  -----------  -----------  -----------  -----------  -----------  -----------  -----------
 1.80000e-01  2.57000e-01  9.87269e-01  9.13704e-01  1.60058e-02  2.87793e-02  1.11539e-01  4.67425e-03  7.39629e-03
 1.80000e-01  2.85000e-01  9.84091e-01  9.17562e-01  1.66126e-02  2.49585e-02  1.13468e-01  4.97769e-03  7.11317e-03
 1.80000e-01  3.10000e-01  9.82494e-01  9.21070e-01  1.71046e-02  2.21598e-02  1.15222e-01  5.22365e-03  6.86953e-03 
 
'''

class ParasticC:

    def __init__(self,folder):
        self.folder = folder
        self.columns = ['Width','Spacing','Ctotal','Cbottom','Ca','Ccoup','Cf']

    def extract(self,base,corner):
        """
        Parastic capacitance should be considered in 3T resistor model.
        Only concern the pizza type(arr_above_gp).
        Only concern the capacitance between conductor and substrate(XXX,above,substrate).
        """
        import pandas as pd
        file = base + '_' + corner
        try:
            content = open(self.folder + '/' + file + '.out','r').readlines()
        except:
            print('\n 未发现文件: %s，请确认是否已将其全部重命名。'%(file+'.out')); exit()
            
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
                    C_aera = content[k+3].split(' ').pop()
                    Width = value[0]
                    dic['Ca'] = eval(C_aera)*eval(Width)

                    for i,x in enumerate(['Width','Spacing','Ctotal','Cbottom','Ccoup','Cf']):
                        dic[x] = eval(value[i])
                    valuelist.append(dic)

        return pd.DataFrame(valuelist,index=conductor,columns=self.columns)

class BlockC:

    def __init__(self,folder):
        self.folder = folder

    def extract(self,struc,content,row):
        if struc == 'Structure-1': columns = ['Width','Spacing','Ctotal','Cbottom','Ca','Ccoup','Cf']
        elif struc == 'Structure-2': columns = ['Width','Spacing','Ctotal','Cbottom','Ctop','Cb_area','Ct_area','Ccoup','Csd','Csu']
        """
        7 rows below 'arr_above_gp'(Structure-1) is data
        8 rows below 'arr_btwn_gps'(Structure-2) is data
        """ 
        next = {'Structure-1':7,'Structure-2':8}
        """
        3 rows below 'arr_above_gp' is C_aera
        3,4 rows below 'arr_btwn_gps' is Cb_area & Ct_area
        """
        if struc == 'Structure-1':
            C_aera = content[row + 3].split(' ').pop()
        elif struc == 'Structure-2':
            Cb_area = content[row + 3].split(' ').pop()
            Ct_area = content[row + 4].split(' ').pop()
        Width = content[row + next[struc]].split(' ')[1]

        spaceN,line = 0,''
        while content[row + next[struc] + spaceN] != '\n':

            value = content[row + next[struc] + spaceN].split(' ')
            while '' in value:
                value.remove('')

            dic = {}
            if struc == 'Structure-1':
                dic['Ca'] = eval(C_aera) * eval(Width)
                for i,x in enumerate(['Width','Spacing','Ctotal','Cbottom','Ccoup','Cf']):
                    dic[x] = eval(value[i])
            elif struc == 'Structure-2':
                dic['Cb_area'] = eval(Cb_area) * eval(Width)
                dic['Ct_area'] = eval(Ct_area) * eval(Width)
                for i,x in enumerate(['Width','Spacing','Ctotal','Cbottom','Ctop','Ccoup','Csd','Csu']):
                    dic[x] = eval(value[i])

            for title in columns:
                if title in ['Width','Spacing']: value = ('%.3f'%dic[title]).ljust(12)
                else: value = format(dic[title],'.2E').ljust(12)
                line = line + value
            line = line + '\n'

            spaceN += 1	

        return line

class QAC:

    def __init__(self,folder):
        self.folder = folder

    def xyw(self,base,corner,up,down,type):
        index = {'Ctotal':2,'Cbottom':3,'Ccoup':4,'Cf':5}[type]
        content = open(self.folder + '/' + base + '_' + corner + '.out','r').readlines()
        for k,line in enumerate(content):
            if 'Actual Structure Name: %s,above,%s'%(up,down) in line:
                dic,x,y = {},[],[]
                dic['width'] = eval(content[k+6].split(' ')[1])

                spaceN = 1
                while content[k+6+spaceN] != '\n':
                    spaceN += 1  

                for i in range(spaceN):
                    values = content[k+6+i].split(' ')
                    while '' in values:
                        values.remove('')
                    """
                    In every block, Width is fixed, variate with Spacing
                    x is Spacing
                    y is the C of different type
                    """
                    x.append(values[1])
                    y.append(values[index])
                dic['x'] = x; dic['y'] = y 
                break
        return dic

    def extract(self,type):
        """
        type: Ctotal/Cbottom/Ccoup/Cf
        only concern the Structure-1 (Pizza)
        """
        content = open(self.folder + '/' + 'AA_TT.out','r').readlines()
        all = []
        """
        all = [ {'TT':{'x':[1,2,3],'y':[1,2,3],'width':100},{'FF':{..}},{'SS':{..}},'title':xxx},
                .....
                .....
              ]
        """
        for k,line in enumerate(content):
            if 'Generic Structure Name: arr_above_gp' in line:
                dic = {}
                down = content[k+1].split(',')[-1]
                up = content[k+1].split(' ').pop().split(',')[0]
                if down == 'substrate\n':
                    title = up + '-AA\n'
                    signal = 1 
                else:
                    title = up + '-' + down	
                    signal = 0 

                for corner in ['TT','FF','SS']:
                    dic[corner] = self.xyw('AA',corner,up,down,type)
                    dic['title'] = type + ' versus Spacing for ' + title
                all.append(dic)
                if signal == 1:
                    for corner in ['TT','FF','SS']:
                        dic[corner] = self.xyw('STI',corner,up,down,type)
                        dic['title'] = type + ' versus Spacing for ' + up + '-STI\n'
                    all.append(dic)
        return all

if __name__ == '__main__':
    import os,sys
    folder = sys.path[0]+'/test'
    result, result2 = ParasticC(folder),BlockC(folder)
    content = open(folder + '/AA_FF.out','r').readlines()
    print(result2.extract('Structure-1',content,188))