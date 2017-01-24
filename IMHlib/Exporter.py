import xlwt

class ParasticCxls:

    def __init__(self,folder):
        self.folder = folder   

    def export(self,DF):
        """
        DF should be a dict as below:
        {'TT': DataFrame of STI_TT extract from Extractor.ParasticC
         'FF': DataFrame of STI_FF extract from Extractor.ParasticC
         'SS': DataFrame of STI_SS extract from Extractor.ParasticC
        }
        """
        from IMHlib.Style import Style
        style1 = Style('Arial','none','none').s
        style2 = Style('Arial',4,'none').s
        style3 = Style('Arial',2,'none').s
        styleTT = Style('Arial','none',171).s
        styleFF = Style('Arial','none',178).s
        styleSS = Style('Arial','none',29).s
        
        def col(x):
            col = ord(x) - ord('A')
            return col
            
        #Generate excel
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet("Resistor's Parastic C",cell_overwrite_ok=True)

        ws.write(0, 0, '***********************')
        ws.write(1, 0, '* Layers: On STI *')
        ws.write(2, 0, '***********************')
        ws.write(0, col('F'), 'um/m', style1)
        ws.write(0, col('G'), 'fF/F', style1)
        ws.write(1, col('F'), 1.00E-06, style1)
        ws.write(1, col('G'), 1.00E-15, style1)
        ws.write_merge(2,2,col('J'),col('M'),'International Units',style3)
        ws.col(1).width = 256*20  

        # 1st table
        for i,x in enumerate(['','','Width','Spacing','Ctotal','Cbottom','Ca','Ccoup','Cf']):
            ws.write(3, i, x, style2)          
        for i,x in enumerate(['Ca','Ccoup','Cf','Cf_total']):
            ws.write(3, col('J')+i, x, style3) 
        for i,x in enumerate(['','Layers','um','um','fF/um','fF/um','fF/um','fF/um','fF/um','F/m^2','F/m','F/m','F/m']):
            ws.write(4, i, x, style1)

        styles=[styleTT,styleFF,styleSS]
        for i,corner in enumerate([DF['TT'],DF['FF'],DF['SS']]):
            layer = len(corner)
            ws.write(5+i*layer, 0, ['TT','FF','SS'][i], styles[i])
            ws.write_merge((5+i*layer)+1, (5+i*layer)+(layer-1), 0, 0,'',style1)

            for j,name in enumerate(corner.index):
                row = 5 + i*layer + j
                ws.write(row, 1, name, styles[i])

                for k,type in enumerate(['Width','Spacing','Ctotal','Cbottom','Ca','Ccoup','Cf']):
                    ws.write(row, 2+k, corner[type][name], styles[i])

                equa = {'J':'G' + str(row+1) + '/' + 'C' + str(row+1) + '*G2/F2/F2',
                        'K':'H' + str(row+1) + '*G2/F2',
                        'L':'I' + str(row+1) + '*G2/F2',
                        'M':'K' + str(row+1) + '+' + 'L' + str(row+1)
                        }
                for key,value in equa.items():
                    ws.write(row, col(key), xlwt.Formula(value), styles[i])
              
        # 2nd table
        for i,x in enumerate(['Interconnect_TT','Interconnect_FF','Interconnect_SS','Resistor_SS','Resistor_FF']):
            ws.write_merge(2, 2, col('P')+2*i, col('Q')+2*i, x, style3)
        for i,x in enumerate(['TT','FCSR','SCFR','FCSR-TT','SCFR-TT']):
            ws.write_merge(3, 3, col('P')+2*i, col('Q')+2*i, x, style3)
        for i,x in enumerate(['Cond-STI','COX','CFOX','COX','CFOX','COX','CFOX','DCOX','DCFOX','DCOX','DCFOX']):
            ws.write(4, col('O')+i, x, style3)
        ws.col(col('Q')).width=256*15

        for i in range(5,5+layer):
            row = i + 1
            equa = {'O':'B' + str(row),
                    'P':'J' + str(row),
                    'Q':'L' + str(row),
                    'R':'J' + str(row + layer),
                    'S':'L' + str(row + layer),
                    'T':'J' + str(row + layer*2),
                    'U':'L' + str(row + layer*2),
                    'V':'R' + str(row) + '-' + 'P' + str(row),
                    'W':'S' + str(row) + '-' + 'Q' + str(row),
                    'X':'T' + str(row) + '-' + 'P' + str(row),
                    'Y':'U' + str(row) + '-' + 'Q' + str(row),
                    }
            for key, value in equa.items():
                if key in ['P','Q']: style = styleTT
                elif key in ['R','S']: style = styleFF
                elif key in ['T','U']: style = styleSS
                else: style = style1
                ws.write(i, col(key), xlwt.Formula(value), style)

        wb.save(self.folder+'/'+'Capacitance For 3T-Resistor.xls')
        print('\n 已完成:\t Capacitance For 3T-Resistor.xls')

class Structure:

    def __init__(self,folder):
        import time
        self.folder = folder
        self.date = time.strftime("%Y-%m-%d",time.localtime(time.time()))

    def export(self,struc):

        from IMHlib.Extractor import BlockC
        blockC = BlockC(self.folder)

        if struc == 'Structure-1': key = 'arr_above_gp'; describe = 'Parallel lines above a bottom plate'
        elif struc == 'Structure-2': key = 'arr_btwn_gps'; describe = 'Parallel lines between two plates'

        f = open(self.folder + '/' + struc + '.txt','w')
        for corner in ['TT','FF','SS']:
            f.write('''
***********************************************************************
********           Interconnect Capacitance Table             *********
***********************************************************************

Process:\t 请搜索全部替换例如："0.18um 1P6M Logic Salicide, Dual Voltage (1.8V/3.3V)"
Version:\t 请搜索全部替换例如：0.3
Date:\t %s
Corner:\t %s
Structure:\t%s
(Please refer to SPICE model document for the definition of each capacitance)\n
                '''%(self.date, corner, '%s (%s)'%(struc,describe)))

            for base in ['AA','STI']:
                content = open(self.folder + '/' + base + '_' + corner + '.out','r').readlines()
                for i,line in enumerate(content):
                    if key in line:

                        if key == 'arr_above_gp':
                            up = content[i+1].split(' ').pop().split(',')[0]
                        elif key == 'arr_btwn_gps':
                            upgather = content[i+1].split(' ').pop().split(',')
                            up = upgather[0] + '-' + upgather[1]

                        down = content[i+1].split(' ').pop().split(',')[-1].rstrip('\n')
                        if down == 'substrate':
                            down = 'AA *'
                        else: down = down + ' *'

                        AcStName = up + '-' + down
                        
                        f.write('''
*************************
* Layers:\t %s
*************************'''%(AcStName))
                        if struc == 'Structure-1':f.write('''
Width       Spacing     Ctotal      Cbottom     Ca          Ccoup       Cf
(um)        (um)        (fF/um)     (fF/um)     (fF/um)     (fF/um)     (fF/um)
--------    --------    --------    --------    --------    --------    --------\n''')
                        elif struc == 'Structure-2':f.write('''
Width       Spacing     Ctotal      Cbottom     Ctop        Cb_area     Ct_area     Ccoup       Csd         Csu
(um)        (um)        (fF/um)     (fF/um)     (fF/um)     (fF/um)     (fF/um)     (fF/um)     (fF/um)     (fF/um)
--------    --------    --------    --------    --------    --------    --------    --------    --------    --------\n''')

                        f.write(blockC.extract(struc,content,i))

                        if struc == 'Structure-1':
                            f.write('--------    --------    --------    --------    --------    --------    --------\n')
                        elif struc == 'Structure-2':
                            f.write('--------    --------    --------    --------    --------    --------    --------    --------    --------    --------\n')
        f.close()
        print('\n 已完成:\t %s.txt'%struc)