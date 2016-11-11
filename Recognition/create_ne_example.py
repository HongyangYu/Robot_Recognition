from random import randint
import os
img_row, img_col = 400, 640
min_example_row, min_example_col = 30, 30
max_example_row, max_example_col = 250, 250

path = 'train'
files = os.listdir(path)

for m_file in files:
    if not m_file.endswith('txt'):
        continue
    else:
        filename = os.path.join( path, m_file )
        fh = open(filename, 'a+' )
        lines = fh.readlines()

        pos = []

        col_max = img_col
        row_max = img_row
        for i in range(len(lines)):
            IsSatisfied = False    
            while(not IsSatisfied):
                ne_pos_x_1 = randint( 0, col_max )
                ne_pos_y_1 = randint( 0, row_max )
                ne_pos_x_2 = ne_pos_x_1 + randint(min_example_col, max_example_col)
                ne_pos_y_2 = ne_pos_y_1 + randint(min_example_row, max_example_row)
                if(ne_pos_x_2 > col_max or ne_pos_y_2 > row_max):
                    continue
                IsSatisfied = True
                for line in lines:
                    vals = line.split(',')
                    pos = [int(val) for val in vals[1:]]
                    bx_1 = pos[0]
                    by_1 = pos[1]
                    bx_2 = pos[2]        
                    by_2 = pos[3]
                    if(bx_1 < ne_pos_x_2 and bx_2 > ne_pos_x_1 \
                       and by_1 < ne_pos_y_2 and by_2 > ne_pos_y_1):
                        IsSatisfied = False
                        break
            newline = '13,{0},{1},{2},{3}\n'.\
            format(ne_pos_x_1,ne_pos_y_1,ne_pos_x_2,ne_pos_y_2)
            fh.write(newline)
        fh.close()



