import xlwt
import os

class PreRun:
		
    def __init__(self,output):
        self.output = output
        self.wb = xlwt.Workbook(encoding='utf-8')
        self.ws = self.wb.add_sheet('pre_run_data',cell_overwrite_ok=True)

        # style
        alignment =	xlwt.Alignment()
        alignment.horz = xlwt.Alignment.HORZ_CENTER
        alignment.vert = xlwt.Alignment.VERT_CENTER
        self.style = xlwt.XFStyle() 
        self.style.alignment = alignment

        # set 2 types, 3 corners, 11 titles：
        self.type = ['AA','STI']
        self.corner = ['Typical','Fast','Slow']
        self.title = ['Dielectic Name','Thickness(um)','Variation(3σ)','Permittivity','Conductor Name','Thickness(um)','Variation(3σ)','Min Width(um)','Variation(3σ)','Min Space(um)','Zmin(um)']

    def write(self,base,corner,DF):
        
        Diel,Cond = DF['Diel'],DF['Cond']
        # location of header
        gapR = len(Diel) + 2 + 2
        gapC = len(self.title) + 2
        locR = {'AA':0,'STI':1}[base] * gapR
        locC = {'Typical':0,'Fast':1,'Slow':2}[corner] * gapC
        # put the name into header, like: AA_Typical
        self.ws.write(locR,locC,base+'_'+corner, self.style)
        # write in the title, set grid's width, according to each title's length
        for k,line in enumerate(self.title):
            self.ws.col(locC+k).width = 256*len(line)
            self.ws.write(locR + 1, locC + k, line, self.style)
        # write in dielectric
        i = 0
        for name,value in Diel.iterrows():
        
            temp = [name,
                    value['thick'],
                    '(±'+str(value['t_varia']*100)+'%)',
                    value['permittivity']
                    ]
                    
            for k,x in enumerate(temp):
                self.ws.write(locR + 2 + i, locC + k, x, self.style)
                
            i += 1
        # write in conductor
        i = 0
        for name,value in Cond.iterrows():
        
            temp = [name,
                    value['thick'],
                    '(±'+str(value['t_varia']*100)+'%)',
                    value['width'],
                    '(±'+str(value['w_varia']*100)+'%)',
                    value['space'],
                    value['Zmin']
                    ]
                    
            for k,x in enumerate(temp):
                self.ws.write(locR + 2 + i, locC + 4 + k, x, self.style)
                
            i += 1

        if base == 'STI' and corner == 'Slow':
            self.wb.save(self.output+'/pre_run_datas.xls')
            print('\n 已完成:\t pre_run_datas.xls')

class TechChar:

    def __init__(self,output):
        self.output = output

    def write(self,base,corner,DF):
        # Generate techChar.tch
        Diel,Cond = DF['Diel'],DF['Cond']

        if os.path.exists(self.output+'/'+base+'_'+corner+',rpd'):
            pass
        else:
            os.mkdir(self.output+'/'+base+'_'+corner+',rpd')

        f=open(self.output+'/'+base+'_'+corner+',rpd/techChar.tch','w')

        f.write('TCH  0007\nCMP 1\n$\n$ Layers\n')
        f.write(str(len(Diel+Cond))+'\n')

        for name,value in Diel.iterrows():
            f.write(name +'\t\t'+'DIEL'+'\n')
        for name,value in Cond.iterrows():
            f.write(name +'\t\t'+'COND'+'\n')

        # write in conductor
        f.write('$\n$ Conductors\n')
        f.write(str(len(Cond))+'\n')
        i = 0
        for name,value in Cond.iterrows():
            f.write('$   (cond '+str(i+1)+')'+'\n')
            f.write(str(len(Diel)+i)+'\t')
            f.write('%.4f'%value['thick'] +'\t')
            f.write('%.4f'%value['Zmin'] +'\t'+'0'+'\t'+'0'+'\n')
            f.write('2\n')
            # width min1 max1 step1 min2 max2 step2 :set by another file:disc.pts
            f.write('\t'+'0'+'\t'+'0'+'\t'+'0'+'\n')
            f.write('\t'+'0'+'\t'+'0'+'\t'+'0'+'\n')
            f.write('2\n')
            # space min1 max1 step1 min2 max2 step2 :set by another file:disc.pts
            f.write('\t'+'0'+'\t'+'0'+'\t'+'0'+'\n')
            f.write('\t'+'0'+'\t'+'0'+'\t'+'0'+'\n')
            i += 1

        # write in dielectric
        f.write('$\n$ Dielectrics\n')
        f.write(str(len(Diel)) +'\n')
        i = 0
        for name,value in Diel.iterrows():
            f.write(str(i)+'\t')
            f.write('%.4f'%value['thick'] +'\t')
            f.write(str(value['permittivity']) +'\t')
            f.write('0  -1'+'\t'+'3'+'\t'+'1.5'+'\n')
            i += 1

        f.close()
        
        if base == 'STI' and corner == 'Slow':
            print('\n 已完成:\t techChar.tch')
            
class Dicspts:
    
    def __init__(self,output):
        self.output = output
    
    def write(self,base,corner,DF):
        """
        Generate disc.pts
        'wb+' means binary format, Raphael only read binary in UNIX
        """
        f = open(self.output+'/'+base+'_'+corner+',rpd/disc.pts','wb+') 	
        """
        Smax : maximal space value
        Snum : the quantity of space
        """
        Smax = 10
        Snum = 15
        # use unlinear function (3/2)^x-1 generate unlinear gap between S and Smax
        def SS(x):
            SS = S + (Smax - S)/((3/2)**(Snum - 2) - 1)*((3/2)**x - 1)
            return '%.3f'% SS

        Cond = DF['Cond']
        for name,value in Cond.iterrows():
            W = '%.3f'% value['width']
            S = value['space']
            # first space should smaller than S
            SubRule	= 0.9 * S
            Spacelist =	['%.3f'% SubRule] + [SS(x) for x in range(Snum-1)]

            f.write(name.encode() + b'\n')
            f.write(b'W'+b'\t'+W.encode()+b'\n')
            f.write(b'S')
            for s in Spacelist:
                f.write(b'\t'+s.encode())
            f.write(b'\n')

        f.close()    

        if base == 'STI' and corner == 'Slow':
            print('\n 已完成:\t disc.pts')