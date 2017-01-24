import xlrd
import pandas as pd

class LayerMessage:

    def __init__(self,file):
        self.wb = xlrd.open_workbook(file)
        # search the sheet whether has a name 'Interconnect' or 'interconnect'
        sheet_list = [line.name for line in self.wb.sheets()]

        if 'interconnect' in sheet_list: 
            self.ws = self.wb.sheet_by_name('interconnect')
        elif 'Interconnect' in sheet_list:
            self.ws = self.wb.sheet_by_name('Interconnect')
        else:
            input("\n Warning: 请将所在 sheet 的名称改为 'interconnect' 或 'Interconnect'.");exit()

        self.Columns = ['thick','t_varia','width','w_varia','space','permittivity','Inter','Zmin']


    def LayerStack(self,type):
        """
        get layer stack information
        first  row is Dielectric layer
        second row is Conductor  layer
        third  row is interlayer layer 
        """
        dic = {'Diel':0,'Cond':1,'Inter':2}
        stack = self.ws.row_values(dic[type])[1:]
        #clean empty values in the list：
        while '' in stack:
            stack.remove('')
        return stack


    def delU(self,num):	
        """
        take off units	
        just like : 3000A -> 3000  ;  (±10%) -> 10
        """
        import re
        m = re.search('\d+(\.\d+)?',str(num))
        if '%' in str(num):
            return eval(m.group())/100
        else:
            return eval(m.group())


    def ExtractValue(self,type):
        """
        type = Diel or Cond
        Original data from excel. keep their unit.
        """
        nums = self.ws.nrows

        Stack = self.LayerStack(type)

        message = []
        for layer in Stack:
            """
            search from the 4th row
            get all elements for the current row
            """
            dic = {}
            for row in range(3,nums):
                values = self.ws.row_values(row)
                if layer in values:
                    position = values.index(layer)
                    """
                    the 1st value after name is thickness
                    ....2nd.....................varition of thick
                    """
                    dic['thick'] = self.delU(values[position + 1])
                    dic['t_varia'] = self.delU(values[position + 2])

                    """
                    for dielectric:
                    ....3rd.....................dielectric permittivity constant
                    for conductor:
                    ....3rd.....................width
                    ....4th.....................varition of width
                    ....5th.....................space
                    """
                    if type == 'Diel':
                        dic['permittivity'] = self.delU(values[position + 3])
                    elif type == 'Cond':
                        dic['width'] = self.delU(values[position + 3])
                        dic['w_varia'] = self.delU(values[position + 4])
                        dic['space'] = self.delU(values[position + 5])
                    break
            message.append(dic)

        message = pd.DataFrame(message,index=Stack,columns=self.Columns)
        if type == 'Cond' : message['Inter'] = self.LayerStack('Inter')

        return message


    def Zmin(self,base,corner,flag):

        Diel = self.ExtractValue('Diel')
        Cond = self.ExtractValue('Cond')
        """
        Calculate the corner's thick, width, space
        transistor is faster/slow as parasitic capacitance is small/large when dielectric is thick/thin
        ..............faster/slow as..........................small/large......conductor.....thin/thick
        ..............faster/slow as..........................small/large......width.........narrow/broad
        ..............faster/slow as..........................small/large......space.........large/small
        """
        DielCor = {'Typical':0,'Fast':1,'Slow':-1}
        CondCor = {'Typical':0,'Fast':-1,'Slow':1}

        Diel['thick'] = Diel['thick'] * (1 + DielCor[corner] * Diel['t_varia']) * 1e-4

        Cond['thick'] = Cond['thick'] * (1 + CondCor[corner] * Cond['t_varia']) * 1e-4
        Cond['width'] = Cond['width'] * (1 + CondCor[corner] * Cond['w_varia'])
        Cond['space'] = Cond['space'] - CondCor[corner] * Cond['width'] * Cond['w_varia']


        if base == 'AA': temp = Diel.drop(Diel.index[0])
        elif base == 'STI': temp = Diel.drop(Diel.index[1])

        Zmin = []
        for nameC,valueC in Cond.iterrows():
            # the first and last conductor are upon the dielectric layer
            if nameC == Cond.index[0]:
                height = temp['thick'][0]
            elif nameC == Cond.index[-1]:
                height = sum(temp[:valueC['Inter']]['thick'])
            # other conductors should consider the Cu/Al process
            else:
                height = sum(temp[:valueC['Inter']]['thick']) - valueC['thick'] * flag
            Zmin.append( height )
        Cond['Zmin'] = Zmin
        
        return {'Diel':temp,'Cond':Cond}


if __name__ == '__main__':
    import os,sys
    file = sys.path[0]+'/Information_test.xlsx'
    result = LayerMessage(file)
    Diel = result.ExtractValue('Diel')
    Cond = result.ExtractValue('Cond')
    Zmin = result.Zmin('AA','Typical',1)
    print(Diel,'\n',Cond,'\n',Zmin)
