from tkinter import filedialog
from pathlib import Path
from tkinter import *
import platform
import os,re

class YouLey:
    def __init__(self, root) -> None:
        self.w = int(root.winfo_screenwidth()/3)
        self.h = int(root.winfo_screenheight()/2.5)
        self.links = []
        
        frameTOP = Frame(root,bg='white')
        frameMIDDLE = Frame(root,bg='white')
        frame = Frame(root,bg='white')

        root.minsize(width=self.w, height=self.h) 
        root.title('YouLey - Baixar Músicas do YouTube')

        frameTOP.pack(side=TOP,expand=True, fill=BOTH)
        frameMIDDLE.pack(sid=TOP,expand=True,fill=BOTH)
        frame.pack(side=TOP,expand=True, fill=BOTH)
        
        self.printLabelEntry1 = Label(frameTOP, text = 'Cole o link  :',bg='white')
        self.printLabelEntry1.pack(side=LEFT,padx=5)

        self.printEntry = Entry(frameTOP, justify=CENTER)
        self.printEntry.pack(side=LEFT,expand=True, fill='x',padx=10, pady=5)
        self.printEntry.bind('<Return>', self.sendToListBox)
        self.printEntry.focus()

        self.printButton = Button(frameTOP, text = 'Adicionar', command=self.sendToListBox)
        self.printButton.pack(side=RIGHT,padx=10)

        self.printLabelEntry1 = Label(frameMIDDLE, text = 'Salvar em  :',bg='white')
        self.printLabelEntry1.pack(side=LEFT,padx=5)

        self.printEntry2 = Entry(frameMIDDLE, justify=CENTER)
        self.printEntry2.pack(side=LEFT,expand=True, fill='x', padx=10)
        self.printEntry2.configure(foreground="gray")
        self.insertEntryDefault()

        self.printButton3 = Button(frameMIDDLE, text = 'Procurar', command=self.browse)
        self.printButton3.pack(side=RIGHT,padx=10)

        self.printListBox = Listbox(frame,justify=CENTER,fg='green',highlightcolor='light green')
        self.printListBox.pack(side=TOP, fill=BOTH, expand=True,padx=10,pady=10)
        self.printListBox.bind('<Delete>',self.deleteSelected)
        self.printListBox.bind('<Return>',self.selected_item)
        #self.printListBox.bind('<<ListboxSelect>>', callback)

        self.printButton2 = Button(frame, text = 'Download')
        self.printButton2.pack(side=TOP,padx=10, pady=10)

    def sendToListBox(self,Event=None):
        #ENVIAR PARA OS LINKS
        link = self.getEntry()
        if ' ' in link:
            self.clearEntry()
            return

        elif link== '':
            self.clearEntry()
            return

        elif len(link) >= 55:
            self.printListBox.insert(0,link[:49]+'...')
            self.clearEntry()

        else:
            self.printListBox.insert(0,link)
            self.clearEntry()

    def getEntry(self):
        return self.printEntry.get()
    
    def clearEntry(self):
        self.printEntry.delete(0, 'end')

    def clearEntry2(self):
        self.printEntry2.delete(0,'end')

    def browse(self):
        download_Directory = filedialog.askdirectory(initialdir=os.getcwd(),title="Selecione canto para baixar as músicas")
        if download_Directory:
            self.clearEntry2()
        self.printEntry2.insert(0,download_Directory)
    
    def insertEntryDefault(self):
        path = str(Path.home() / "Downloads")
        if self.checkSystem() == 'Windows':
            print('windows')
            self.printEntry2.insert(0,path)
        else:
            print('linux')
            self.printEntry2.insert(0,path)

    def checkSystem(self):
        return platform.system()

    def deleteSelected(self,Event=None):
        self.printListBox.delete(ANCHOR)

    def selected_item(self,Event=None):
        for i in self.printListBox.curselection():
            print(self.printListBox.get(i))
