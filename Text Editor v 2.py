# a Text editor like Notepad using tkinter Python (version v.2.1)
# used a more modern python GUI module tkinter
# tested with python 32 13aug2016
# fixed all bugs and works successfully
# author SHAROOK 



from tkinter import *
from tkinter.filedialog import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import *


#class main(Frame):
class main:

    def __init__(self):
        #Frame.__init__(self,parent)
        self.parent=Tk()
        #self.parent.withdraw()
        #self.parent=parent
        self.parent.title('new Text Editor')
        self.parent.minsize(width=650,height=550)
        self.frame=Frame(self.parent)
        self.display()
        self.frame.pack(fill=BOTH,expand=True)
        
        self.parent.bind('<Button-3>',self.rightclick)

        self.parent.bind('<Control-n>',self.newfile)
        self.parent.bind('<Control-o>',self.openfile)
        self.parent.bind('<Control-s>',self.save)
        self.parent.bind('<Control-Shift-S>',self.savefile)
        self.parent.bind('<Control-q>',self.quit)

        self.parent.bind('<Control-z>','undocallback')
        self.parent.bind('<Control-x>',self.cutmenu)
        self.parent.bind('<Control-c>','self.copymenu')
        self.parent.bind('<Control-v>','self.pastemenu')
        self.parent.bind('<Delete>',self.deletemenu)
        self.parent.bind('<Control-f>',self.findmenu)
        
        self.parent.protocol('WM_DELETE_WINDOW',self.quit)
        self.parent.mainloop()

        
    def display(self):
        self.scroll=Scrollbar(self.parent,orient=VERTICAL)
        self.scroll.pack(side=RIGHT,fill=Y)

        self.scroll2=Scrollbar(self.parent,orient=HORIZONTAL)
        self.scroll2.pack(side=BOTTOM,fill=X)

        self.text=Text(self.frame,undo=True,wrap='none',xscrollcommand=self.scroll2.set,yscrollcommand=self.scroll.set)
        self.text.pack(fill=BOTH,expand=True)
    
        self.scroll.config(command=self.text.yview)
        self.scroll2.config(command=self.text.xview)

        self.menubar=Menu(self.parent)
        self.parent.config(menu=self.menubar)

        self.filemenu=Menu(self.menubar)
        self.menubar.add_cascade(label='File',menu=self.filemenu)
        self.filemenu.add_command(label='New',accelerator='Ctrl+N',command=self.newfile)
        self.filemenu.add_command(label='Open',accelerator='Ctrl+O',command=self.openfile)
        self.filemenu.add_command(label='Save',accelerator='Ctrl+S',command=self.save)
        self.filemenu.add_command(label='Save as',accelerator='Ctrl+Shft+S',command=self.savefile)
        self.filemenu.add_separator()
        #filemenu.add_command(label='Print',command='donothing')
        #filemenu.add_separator()
        self.filemenu.add_command(label='Exit',command=self.quit)
        

        self.filemenu=Menu(self.menubar)
        self.menubar.add_cascade(label='Edit',menu=self.filemenu)
        self.filemenu.add_command(label='Undo',accelerator='Ctrl+Z',command=self.undo)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Cut',accelerator='Ctrl+X',command=self.cutmenu)
        self.filemenu.add_command(label='Copy',accelerator='Ctrl+C',command=self.copymenu)
        self.filemenu.add_command(label='Paste',accelerator='Ctrl+V',command=self.pastemenu)
        self.filemenu.add_command(label='Delete',accelerator='Del',command=self.deletemenu)
        self.filemenu.add_separator()
        self.filemenu.add_command(label='Find',command=self.findmenu)

        self.filemenu=Menu(self.menubar)
        self.menubar.add_cascade(label='View',menu=self.filemenu)
        self.filemenu.add_command(label='Font',command='donothing')
        self.filemenu.add_separator()

        self.filemenu=Menu(self.menubar)
        self.menubar.add_cascade(label='Help',menu=self.filemenu)
        self.filemenu.add_command(label='about Text Editor',command='donothing')
        self.filemenu.add_separator()
        self.filemenu.add_command(label='about Developer',command='donothing')
    

        
    def openfile(self,event=None):
        try:
            self.name=askopenfilename(parent=self.parent,filetypes=(('Text File','*.txt'),('All Files','*.*')),title='Open')
            print(self.name)
            fo=open(self.name,'r')
            filecontent=fo.read()
            if(self.text.get(1.0,END)=='\n'):
                self.text.insert(1.0,filecontent)
            else:
                self.exitfile()
                self.text.delete(1.0,END)
                self.text.insert(1.0,filecontent)
            de=str.split(self.name,'/')
            de=de[len(de)-1]
            de=str.split(de,'.')
            self.parent.title(de[0]+' - Text Editor')
            global name
        except UnicodeDecodeError:
            showwarning('Open','Cannot Open the file')
            pass
        except:
            pass
        self.text.edit_modified(False)
        '''except:
            print('no file selected')
            pass'''
            

    def newfile(self,event=None):
        #self.newwindow=Toplevel()
        #self.app=temp(self.parent)
        main()
        
    def save(self,event=None):
        try:
            if(self.name):
                fo=open(self.name,'w')
                text2save=str(self.text.get(1.0,END))
                fo.write(text2save)
            '''except IOError:
            showwarning('save as','Cannot save the file')
            pass'''
        except:
            self.savefile()
        self.text.edit_modified(False)


    def savefile(self,event=None):
        try:
            fout=asksaveasfilename(parent=self.parent,defaultextension='.txt')
            file=open(fout,'w')
            text2save=str(self.text.get(1.0,END))
            file.write(text2save)
            print(fout)
            self.name=fout
            de=str.split(fout,'/')
            de=de[len(de)-1]
            de=str.split(de,'.')
            self.parent.title(de[0]+' - Text Editor')
        except IOError:
            showwarning('save as','File is Not saved ')
            pass
        self.text.edit_modified(False)
        
    def exitfile(self):
        if (self.text.edit_modified()):
            #print(self.text.edit_modified())
            s=messagebox.Message(title='Warning',message='Document modified. Save changes?',type=messagebox.YESNOCANCEL).show()
            if(s=='yes'):
                self.save()
                return True
                #self.parent.destroy()
            elif(s=='cancel'):
                pass
            elif(s=='no'):
                return True
                #self.parent.destroy()
        else:
            return 'no'
    

    def quit(self,event=None):
        if(self.exitfile()):
            self.parent.destroy()
        else:
            pass

    def undo(self):
        self.text.edit_undo()

    def cutmenu(self,event=None):
        try:
            self.copymenu()
            self.text.delete('sel.first','sel.last')
        except:
            pass

    def copymenu(self,event=None):
        global temp
        try:
            #text._clipboard=text.get('sel.first','sel.last')
            temp=self.text.get('sel.first','sel.last')
            print(temp)
            #self.clipboard_clear()
            #clipboard_append(self.text.get(SEL_FIRST,SEL_LAST))
            #print(text._clipboard)
        except:
            print("nothing selected")
            pass

    def pastemenu(self,event=None):
        try:
            #print(temp)
            self.text.insert(INSERT,temp)
            #self.text.insert(INSERT,selection_get(selection='CLIPBOARD'))
        except:
            pass

    def deletemenu(self,event=None):
        try:
            text.delete('sel.first','sel.last') 
        except:
            pass


    def findmenu(self,event=None):
        try:
            target=askstring('Find','Find What?')
            print(target)
            if target:
                past=1.0
                self.text.tag_delete('tag',1.0,END)
                while(True):
                    where=self.text.search(target,past,END)
                    print(where)
                    if(where!=END):
                        de=str.split(where,'.')
                        d=int(de[1])
                        print(d)
                        past=d+len(target)
                        past=str(de[0])+'.'+str(past)
                        self.text.tag_add('tag',where,past)
                        self.text.tag_config('tag',background='yellow',foreground='red')
                        #where=past
                    #else:
                       # break
        except:
            pass

    def rightclick(self,event):
        print('right button clicked')
        self.popup=Menu(self.parent,tearoff=0)
        self.popup.add_command(label='undo',command='self.undo')
        self.popup.add_command(label='cut',command='self.cutmenu')
        self.popup.add_command(label='copy',command='self.copymenu')
        self.popup.add_command(label='paste',command='self.pastemenu')
        self.popup.add_command(label='delete',command='self.deletemenu')
        self.popup.add_command(label='find',command='self.findmenu')
        
        try:
            self.popup.tk_popup(event.x,event.y,0)
            #x,y=event.x,event.y
            #x,y=x+x,y+y
            #popup.post(x,y,0)
            #print(event.x,event.y)
        finally:
            self.popup.grab_release()

    #def Cancel(Exception):
        #pass


'''class Cancel(Exception):
    pass'''
        
'''class temp:
    def __init__(self,parent):
        self.parent=parent
        main()'''
        
if __name__=='__main__':
    '''root=Tk()
    root.title('new Text Editor')
    root.minsize(width=650,height=550)
    main(root)
    root.mainloop()'''
    main()



# i am trying to extend it's features
