
import xlwt

class Style:
    # define the excel unit grid's style
    def __init__(self,fontName,fontColor,pattenColor):

        alignment       = xlwt.Alignment()
        alignment.horz  = xlwt.Alignment.HORZ_CENTER
        alignment.vert  = xlwt.Alignment.VERT_CENTER

        borders         = xlwt.Borders()
        borders.left    = 1
        borders.right   = 1
        borders.top     = 1
        borders.bottom  = 1    

        '''
        name: 'Arial'
        fontColor: 4(blue),2(red)
        '''
        font                = xlwt.Font()
        font.name           = fontName
        font.colour_index   = fontColor

        '''
        pattern_fore_colour:
        171 :   yellow
        178 :   green
        29  :   pink
        42  :   shallow green
        52  :   shallow pink
        '''
        pattern             = xlwt.Pattern()
        pattern.pattern     = 1
        xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_fore_colour = pattenColor

        self.s              = xlwt.XFStyle()
        self.s.alignment    = alignment
        self.s.borders      = borders
        if fontColor == 'none':pass
        else: self.s.font    = font
        if pattenColor == 'none':pass
        else: self.s.pattern = pattern

if __name__ == '__main__':
    wb = xlwt.Workbook(encoding='utf-8')    
    ws = wb.add_sheet("sheet",cell_overwrite_ok=True)
    ws.write(0,0,'test',Style('Arial',4,171).s)
    wb.save('D:/test.xls')