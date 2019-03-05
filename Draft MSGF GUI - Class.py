from tkinter import *
import pandas as pd
import numpy as np
import tempfile

t = tempfile.TemporaryFile(mode="r+")
f = open("C://Users//apablo1//Documents//Scripts//MSGF modifications.txt", 'r')
MSGF_lines = f.readlines()
f.seek(0)
for line in f:
    t.write(line.rstrip() + '\n')
 
f.close()

mods = []
untag = []
tag = []

class New_Process_Pipeline():
    def __init__(self):
        self.blank = Tk()
        self.blank.title('MSGF GUI')
        self.MSGF_Frame = LabelFrame(self.blank, text = 'Select Modification(s) then click "Select" button. Click "Close" to close out.', height = 100, width = 500, bd = 5, font = 'bold')
        self.MSGF_Frame.grid()
        self.d = {}
        flag = False
        for line in MSGF_lines:
            line = line.strip()
    
            if line == '#-# modifications':
                flag = True
                continue
        
            if line == '#-# search parameters':
                break
        
            if flag:
                if line != '':
                    mods.append(line.split('\t')[0].strip())
                    my_list = [i for i, x in enumerate(mods) if x[0] != '#']

        for mod in mods:
            if mod[0] != '#':
                untag.append(mod)
                self.d = {key: 1 for key in untag}
            else:
                tag.append(mod[2:])
                self.c = {key: 0 for key in tag}
                untag.append(mod[2:])
                
        self.d.update(self.c)
        
        def get_MSGF():
            df = pd.DataFrame(self.d.items(), columns=['Tag', 'Status'])
            sorterIndex = dict(zip(untag,range(len(untag))))
            df['Sort'] = df['Tag'].map(sorterIndex)
            df.sort_values(['Sort'], ascending = [True], inplace = True)
            df.drop('Sort', 1, inplace = True)
            df.reset_index(drop=True, inplace = True)
            df['Tagged'] = '# ' + df['Tag'].astype(str)
            new_list = map((lambda var: var.get()), self.CheckVar)
            # print new_list
            df['In'] = np.where(df['Status']==0, df['Tagged'], df['Tag'])
            df['Status'] =  new_list
            df['Out'] = np.where(df['Status']==0, df['Tagged'], df['Tag'])
            Dictionary = df.set_index('In')['Out'].to_dict()
            t.seek(0)
            o = open("C://Users//apablo1//Documents//Scripts//MSGF modifications.txt", "w")
            for line in t:
                line = line.strip('\t')
                if not line:
                    continue
                for key, value in Dictionary.items():
                    if key in line:
                        line = line.replace(key, value)
                o.write(line)
            t.close()         


        self.CheckVar = []

        for x in range(len(untag)):
            row = int(x/5)
            col = x%5
            var = IntVar()
            l = Checkbutton(self.MSGF_Frame, text=untag[x], variable= var, padx = 5, pady = 10, onvalue =1, offvalue=0)
            l.grid(row = row, column = col, sticky = W)
            self.CheckVar.append(var)

           

        self.toolbar = Frame(self.blank, height = 50, width = 225)
        self.CancelButt = Button(self.toolbar, text="Close", command = self.blank.destroy, bg = 'red', fg = 'white', activeforeground = 'red', width = 12)
        self.CancelButt.grid(sticky= E, padx=2, pady=15, row = 1, column = 1)

        self.SendButt = Button(self.toolbar, text="Select", command = get_MSGF, bg = 'blue', fg = 'white', activeforeground = 'blue', width = 12)
        self.SendButt.grid(sticky= W, padx=2, pady=15, row=1, column = 0)
    
        self.toolbar.grid(row=1, column = 0, sticky = SE)
        self.toolbar.grid_propagate(0)

        for x in range(len(self.CheckVar)):
            for y in my_list:
                if x == y:
                    self.CheckVar[x].set(1)

        self.blank.mainloop()


if __name__ == '__main__':
    app = New_Process_Pipeline()