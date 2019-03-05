import re
import tempfile
import pandas as pd
import numpy as np
import tkMessageBox
from tkinter import *

t = tempfile.TemporaryFile(mode="r+")
f = open("C://Path_to_MSGF_File//msgf_mods.txt", 'r')
MSGF_lines = f.readlines()
f.seek(0)
for line in f:
    t.write(line.rstrip() + '\n')
 
f.close()

mods = []
hashed = []
unhashed =[]

class New_Process_Pipeline():
    def __init__(self):
        self.root = Tk()
        self.root.title('MSGF GUI')
        self.root.geometry('+200+0')

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

        for item in mods:
            if item[0] == '#':
                x = item[2:]
                y = x.split(',')
                hashed.append(y[4] + ", " + y[0] + ", " + y[1] + ", " + y[3] +", " + y[2])
            else:
                z = item.split(',')
                unhashed.append(z[4] + ", " + z[0] + ", " + z[1] + ", " + z[3] +", " + z[2])

        #Lists for listbox
        final_list1 = sorted(hashed, key=str.lower)
        final_list2 = sorted(unhashed, key=str.lower)
        
        #List for dataframe for Unimod entry
        final_list = hashed
        final_list.extend(unhashed)
        final_list = sorted(final_list, key = str.lower)
        
    #Begin List Box frame
        self.blank = LabelFrame(self.root, text = 'Select Modifications',
                    height = 500, bd = 3, font = ("Helvetica", 12, "bold"))
        self.blank.grid(row = 0)

        ############## Listbox Frame Functions ##############
            # -> (R) button
        def get_selection():    
            update = []
            allitems2 = self.l2.get(0, END)
            allitems2 = list(allitems2)
            self.l2.delete(0,END)
            allitems = self.l1.get(0, END)
            items = [allitems[int(item)] for item in self.l1.curselection()]
            sel = self.l1.curselection()
            for item in items:
                allitems2.append(item)
            unhashed_inter = set(allitems2)
            unhashed_inter = list(unhashed_inter)
            update = sorted(unhashed_inter, key=str.lower)
            for index in sel[::-1]:
                self.l1.delete(index)
            for item in update:
                self.l2.insert(END, item)


            # <- (L) button
        def remove_selection():
            remove = []
            allitems1 = self.l1.get(0, END)
            allitems1 = list(allitems1)
            self.l1.delete(0, END)
            allitems2 = self.l2.get(0, END)
            items2 = [allitems2[int(item)] for item in self.l2.curselection()]
            sel2 = self.l2.curselection()
            for item in items2:
                allitems1.append(item)
            hashed_inter = set(allitems1)
            hashed_inter = list(hashed_inter)
            remove = sorted(hashed_inter, key=str.lower)
            for index in sel2[::-1]:
                self.l2.delete(index)
            for item in remove:
                self.l1.insert(END, item)


        def select_mods():
            mod_avail = []
            mod_sel_list = []
            mod_dict ={}
            sec_dict = {}
            tagged = self.l1.get(0, END)
            tagged = list(tagged)
            for item in tagged:
                lt = item.split(', ')
                mod_avail.append(lt[1] + "," + lt[2] + "," + lt[4] + "," + lt[3] +"," + lt[0])
     
            mod_dict = {key: 1 for key in mod_avail}
            untagged = self.l2.get(0, END)
            untagged = list(untagged)
            for item in untagged:
                lu = item.split(', ')
                mod_sel_list.append(lu[1] + "," + lu[2] + "," + lu[4] + "," + lu[3] +"," + lu[0])
    
            sec_dict = {key: 0 for key in mod_sel_list}
    
            mod_dict.update(sec_dict)
            df = pd.DataFrame(mod_dict.items(), columns=['Tag', 'Status'])
            listed = [item.replace('# ', '') for item in mods]
            sorterIndex = dict(zip(listed,range(len(listed))))
            df['Sort'] = df['Tag'].map(sorterIndex)
            df.sort_values(['Sort'], ascending = True, inplace = True)
            df.drop('Sort', 1, inplace = True)
            df.reset_index(drop=True, inplace = True)
            df['Tagged'] = '# ' + df['Tag'].astype(str)
            se = pd.Series(mods)
            df['In'] = se.values
            df['Out'] = np.where(df['Status']==1, df['Tagged'], df['Tag'])
            Dictionary = df.set_index('In')['Out'].to_dict()
            t.seek(0)
            o = open("C://Path_to_MSGF_File//msgf_mods.txt"", "w")
            for line in t:
                line = line.strip('\t')
                if not line:
                    continue
                for key, value in Dictionary.items():
                    if key in line:
                        line = line.replace(key, value)
                o.write(line)
            t.close()
        ########## End Space for Functions #########

        #Labels for listboxes
        self.AvailableLabel = Label(self.blank, text="Available Modifications", font = ('Helvetica', 10, 'bold italic'))
        self.AvailableLabel.grid(row = 0, column = 0)
        self.SelectedLabel = Label(self.blank, text="Selected Modifications", font = ('Helvetica', 10, 'bold italic'))
        self.SelectedLabel.grid(row = 0, column = 3)


        #Listbox 1 and scrollbar
        self.l1 = Listbox(self.blank, height = 22, width = 42, font = ('Garamond', 13), selectmode = MULTIPLE)
        for item in final_list1:
            self.l1.insert(END, item)
        self.l1.grid(row=1, column=0, padx = (8,0), pady = 5)
        self.l1_scrollbar = Scrollbar(self.blank, orient="vertical")
        self.l1_scrollbar.config(command=self.l1.yview)
        self.l1_scrollbar.grid(sticky = NS, row = 1, column = 1, pady = 5)
        self.l1.config(yscrollcommand=self.l1_scrollbar.set)

        #Listbox 2 and scrollbar
        self.l2 = Listbox(self.blank, height = 22, width = 42, font = ('Garamond', 13), selectmode = MULTIPLE)
        for item in final_list2:
            self.l2.insert(END, item)
        self.l2.grid(row=1, column=3, pady = 5)
        self.l2_scrollbar = Scrollbar(self.blank, orient="vertical")
        self.l2_scrollbar.config(command=self.l2.yview)
        self.l2_scrollbar.grid(sticky = NS, row = 1, column = 4, padx = (0,8), pady = 5)
        self.l2.config(yscrollcommand=self.l2_scrollbar.set)

        #blank frames that hold the R/L buttons and Select/Close buttons
        self.toolbar = Frame(self.blank, height = 75, width = 40)
        # self.bartool = Frame(self.root, height = 50, width = 225)

        #Send Right
        self.Shift_Right = Button(self.toolbar, text="->", command = get_selection)
        self.Shift_Right.grid(padx = (8,4), row = 0, column = 0)

        #Send Left
        self.Shift_Left = Button(self.toolbar, text="<-", command = remove_selection)
        self.Shift_Left.grid(pady=5, padx = (8,4), row = 1, column = 0)

        #Close out 
        self.CancelButt = Button(self.root, text="Close", command = self.root.destroy, bg = 'red', fg = 'white', activeforeground = 'red', width = 12)
        self.CancelButt.grid(sticky= E, padx=2, pady=15, row = 2, column = 0)

        #Modify Modifications Button
        self.SendButt = Button(self.blank, text="Select", bg = 'blue', fg = 'white', activeforeground = 'blue', width = 12, command = select_mods)
        self.SendButt.grid(sticky= E, padx=2, pady=15, row=3, column = 3)

        #### Instructions ######
        self.Instruction = Label(self.blank, text="Please limit the number of modifications to 3. If this value is large, the search takes long. \n Once you have selected the modifications, press the 'Select' button.",
                    font = ('Helvetica', 11, 'italic'), fg = 'red')
        self.Instruction.grid(row = 2, column = 0, columnspan = 4, pady = 15)

        self.toolbar.grid(row=1, column = 2)
        self.toolbar.grid_propagate(0)

    ## End Listbox frame ##
    
    # Begin Entry GUI frame ##
        #validate the mass units, max number of decimal places in Unimod is 6
        def callback(sv):
            c = sv.get()[0:10]
            sv.set(c)
        
        def update_checkbutton(event=None):
            if self.var.get() == '*, Any':
                self.radioa.config(state=DISABLED)# Needed to set spinbox value = 1
                self.radioa.deselect()
            else:
                self.radioa.config(state='normal')
            
        def grab():
            number = self.massu.get()
            chars = set('.')
            if any((c in chars) for c in number):
                result = re.search('\.'+'(.*)', number)
                length = len(result.group(1))
                ## Check decimal places without converting to floats
                if length <= 3:
                    tkMessageBox.showinfo("Error!", "Need at least 4 decimal places.")
                    return False
                elif length > 6:
                    tkMessageBox.showinfo("Error!", "MSGF does not support more than 6 decimal places.")
                    return False
                elif length == 4:
                    decimal_length = 4
                    four = float(number)
                    newmass = int(four * 10**4)

                elif length == 5:
                    decimal_length = 5
                    five = float(number)
                    newmass = int(five * 10**5)

                elif length == 6:
                    decimal_length = 6
                    six = float(number)
                    newmass = int(six * 10**6)

            else:
                tkMessageBox.showinfo("Error!", "Integer masses are insufficient.")
                return False
            
            df_e = pd.DataFrame({'Mods':final_list})
            df_e = df_e['Mods'].str.split(',', expand=True)
            df_1sp = df_e[1].str.split('.', expand = True)    
            df_1sp[1] = df_1sp[1].str[0:decimal_length]
            df_1sp['Combo'] = df_1sp.fillna('').sum(axis=1)
            df_e[1] = df_1sp['Combo']
            df_e = df_e.apply(lambda x: x.str.strip() if x.dtype == 'object' else x)
            dfList = df_e[1].tolist()
            compList = []
            for value in dfList:
                try:
                    compList.append(int(value))
                except ValueError:
                    compList.append(value)        
            df_e[1] = compList
            
            aminoletter = self.var.get()
            aminoletter = aminoletter.split(',')[0]
            
            if psi_ms.get() == '':
                tkMessageBox.showinfo("Error!", "Please enter a Unimod name.")
                return False
            else:
                unimod_name = psi_ms.get()
                        
            if self.varMod.get() == '':
                tkMessageBox.showinfo("Error!", "Please select a modification type.")
                return False
            else:
                modification_type = self.varMod.get()
        
            if self.PositVar.get() == '':
                tkMessageBox.showinfo("Error!", "Please select a position site.")
                return False
            else:
                attached_position = self.PositVar.get()

            
            def MSGF_2_add():
                MSGF_addition = ('# ' + self.massu.get() + 
                                ',' + aminoletter + 
                                ',' + attached_position + 
                                ',' + modification_type + 
                                ',' + unimod_name +
                                '\t\t\t# ' + self.description_var.get() + ' ' + aminoletter + '\n')
                with open("C://Path_to_MSGF_File//msgf_mods.txt", "r+") as new_f:
                    MSGF_newlines = new_f.readlines()
                    new_f.seek(0)
                    if modification_type == 'fix':
                        fix_indices = [i for i, s in enumerate(MSGF_newlines) if 'fix,' in s]
                        position = fix_indices[-1]+1
                    else:
                        opt_indices = [i for i, s in enumerate(MSGF_newlines) if 'opt,' in s]
                        position = opt_indices[-1]+1
                    MSGF_newlines.insert(position, MSGF_addition)
                    new_f.writelines(MSGF_newlines)
                    new_f.truncate()
            
            if newmass in df_e.values:
                already = df_e.index[df_e[1] == z].tolist()
                # print already
                for x in already:
                    output_zero = df_e.iloc[(x)][0]
                    zero_list = []
                    zero_list.append(output_zero)
                    output_zero = set(zero_list)
                    output_one = df_e.iloc[(x)][2]
                    output_two = df_e.iloc[(x)][3]
                    output_three = df_e.iloc[(x)][4]
                output_zero = list(output_zero) 
                if output_zero == unimod_name:
                    if output_one == aminoletter:
                        if output_two == attached_position:
                            if output_three == modification_type:
                                tkMessageBox.showinfo("Error!", "Value already exist. Please edit the entry.")
                                return False 
                            else:
                                MSGF_2_add()

                        else:
                            MSGF_2_add()
                    else:
                        MSGF_2_add()
                else:
                    tkMessageBox.showinfo("Error!", "Please enter a more precise mass and/or ensure mass is for this Unimod")
                    return False

            elif unimod_name in df_e.values:
                tkMessageBox.showinfo('Warning!', "This Unimod already exists with mass {}. \n Please edit entry with this mass.".format(z))
                return False
            else:
                MSGF_2_add()

        def validate(value_if_allowed):
            if re.match(r'^[0-9\.]*$',value_if_allowed):
                if not value_if_allowed:
                    return True
                try:
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False

        def validate2(value_if_allowed, text):
            if all(x.isalnum() for x in text):
                if not value_if_allowed:
                    return True
                try:
                    str(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        ###End of GUI entry definitions##

        self.panel2 = LabelFrame(self.root, text = 'Enter New Modification', height = 200, bd = 3, font = ("Helvetica", 12, "bold"))
        self.panel2.grid(row = 1)
   
        self.Butt = Button(self.panel2, text="Add", bg = 'blue', fg = 'white', activeforeground = 'blue', width = 12, command = grab)
        self.Butt.grid(sticky=N, padx=(50,0), pady=15, row = 6, column = 4)
        
        ######## Unimod name ###################
        vcmd2 = (self.root.register(validate2), '%P', '%S')
        psi_ms = StringVar()
        self.Unimod = Entry(self.panel2, validate = 'key', validatecommand = vcmd2, textvariable = psi_ms, width = 25)
        self.Unimod.grid(row = 1, column = 0, padx = 15)
        
         ########### Mass entry #################
        vcmd = (self.root.register(validate), '%P')
        sv = StringVar()
        sv.trace("w", lambda name, index, mode, sv=sv: callback(sv))
        self.massu = Entry(self.panel2, validate = 'key', validatecommand = vcmd, textvariable=sv)
        self.massu.grid(row = 1, column = 1, padx = 15)
       
        #####Spinbox of the Amino Acids #############
        Amino_Acids = ['*, Any', 'A, Alanine','R, Arginine','N, Asparagine','D, Aspartic Acid',
                        'C, Cysteine','E, Glutamic Acid','Q, Glutamine','G, Glycine','H, Histidine','I, Isoleucine',
                        'L, Leucine','K, Lysine','M, Methionine','F, Phenylalanine','P, Proline',
                        'S, Serine','T, Threonine','W, Tryptophan','Y, Tyrosine','V, Valine']
        Amino_Acids = Amino_Acids[::-1]
        self.var = StringVar()
        self.spin = Spinbox(self.panel2, textvariable = self.var, values= Amino_Acids, wrap= True, readonlybackground = 'white', state = 'readonly', command=update_checkbutton)
        self.var.set(Amino_Acids[-1])
        self.spin.grid(row = 1, column = 2, padx = 15)
        
        #Buttons for the Position e.g. N-term, C-term etc
        self.posit_toolbar = Frame(self.panel2, height = 40, width = 70)
        self.posit_toolbar.grid(row = 3, column = 0, columnspan = 2)
        self.PositVar = StringVar()
        self.radioa = Radiobutton(self.posit_toolbar, text="Anywhere", variable = self.PositVar, value ='any', tristatevalue = 'w')
        self.radiob = Radiobutton(self.posit_toolbar, text="- OMIT", variable = self.PositVar, value ='-', tristatevalue = 'w')
        self.radioc = Radiobutton(self.posit_toolbar, text="Peptide N-term", variable = self.PositVar, value ='N-term', tristatevalue = 'w')
        self.radiod = Radiobutton(self.posit_toolbar, text="Peptide C-term", variable = self.PositVar, value ='C-term', tristatevalue = 'w')
        self.radioe = Radiobutton(self.posit_toolbar, text="Protein N-term", variable = self.PositVar, value ='Prot-N-term', tristatevalue = 'w')
        self.radiof = Radiobutton(self.posit_toolbar, text="Protein C-term", variable = self.PositVar, value ='Prot-C-term', tristatevalue = 'w')
        self.radioa.config(state = DISABLED)
        self.radioa.grid(row = 0, column=0, sticky = W)
        self.radiob.grid(row = 1, column=0, sticky = W)
        self.radioc.grid(row = 0, column=1, sticky = W)
        self.radiod.grid(row = 1, column=1, sticky = W)
        self.radioe.grid(row = 0, column=2, sticky = W)
        self.radiof.grid(row = 1, column=2, sticky = W)
        
        ### Modification Type ######
        self.type_toolbar = Frame(self.panel2, height = 40, width = 50)
        self.type_toolbar.grid(row = 3, column = 2)        
        self.varMod = StringVar()
        self.PostFix = Radiobutton(self.type_toolbar, text='Fixed', variable=self.varMod, value ='fix', tristatevalue = 'x')
        self.PostFix.grid(row = 0, sticky = W)
        self.PostOpt = Radiobutton(self.type_toolbar, text='Variable', variable=self.varMod, value='opt', tristatevalue = 'x')
        self.PostOpt.grid(row = 1,sticky = E)
        
        ########## Description Widget #############
        self.description_var = StringVar()
        self.description = Entry(self.panel2, textvariable = self.description_var, width = 40)
        self.description.grid(row = 3, column = 3, columnspan = 2, padx = 15)
        
        ########### Instructions #############
        self.InstructionEntry = Label(self.panel2, text="Name: For proper mzIdentML output, this name should be the same as the Unimod PSI-MS name.\nMass: It is important to specify accurate masses. Also, please see list above for masses already entered.\nAmino Acid: * is applicable to any residue. Warning: * and 'anywhere' modification not allowed.\nYou may paste (Ctrl-V) values into the entry box(es), but it wont accept words with spaces at the tail end.\n\nFor Unimod name, mass, and descriptions, please visit http://www.unimod.org/",
                    font = ('Helvetica', 9, 'italic'), fg = 'red', anchor = W, justify = LEFT)
        self.InstructionEntry.grid(row =6, column = 0, columnspan = 4, pady = 15)

        ##### Labels of entry widgets
        self.unimodlabel = Label(self.panel2, text = "Unimod PSI-MS Name", font = ('Helvetica', 10, 'italic'))
        self.unimodlabel.grid(row = 0, column = 0, padx = 15, pady = (10,5))        
        self.masslabel = Label(self.panel2, text="Enter Mass", font = ('Helvetica', 10, 'italic'))
        self.masslabel.grid(row = 0, column = 1, padx = 15, pady = (10,5))
        self.aminoAlabel = Label(self.panel2, text="Amino Acid", font = ('Helvetica', 10, 'italic'))
        self.aminoAlabel.grid(row = 0, column = 2, padx = 15, pady = (10,5))
        self.positionlabel = Label(self.panel2, text="Peptide Position", font = ('Helvetica', 10, 'italic'))
        self.positionlabel.grid(row = 2, column = 0, columnspan = 2, pady = (15,5))
        self.typelabel = Label(self.panel2, text="Modification Type", font = ('Helvetica', 10, 'italic'))
        self.typelabel.grid(row = 2, column = 2, pady = (15,5))
        self.descriptionlabel = Label(self.panel2, text='Short Description', font = ('Helvetica', 10, 'italic'))
        self.descriptionlabel.grid(row = 2, column = 3, columnspan = 2, pady = (15,5))

                
        self.blank.mainloop()
        self.panel2.mainloop()
        
if __name__ == '__main__':
    app = New_Process_Pipeline()