from tkinter import messagebox, filedialog
from pytube import YouTube,Playlist
from pathlib import Path
from tkinter import ttk
from tkinter import *
import tkinter as tk
import re,os,threading

threads = []
links = []
tits = []

atual = 0

def openNewWindow():
    newWindow = Toplevel(root)
    newWindow.title("New Window")
    newWindow.geometry("200x200")

def startThreadProcess():
    myNewThread = threading.Thread(target=Download)
    threads.append(myNewThread)
    myNewThread.start()
    
def startThreadProcessToAdd(Event=None):
    myNewThreadToAdd = threading.Thread(target=add_item)
    threads.append(myNewThreadToAdd)
    myNewThreadToAdd.start()
    
def add_item(Event=None):
    target = linkText.get()
    x = str(re.findall("playlist", target))
    
    #Se for playlist
    if 'playlist' in x:
        print('é uma playlist')
        #Baixa playlist
        p = Playlist(target)
        try:
            for url in p.video_urls:
                links.append(str(url))
                yt = YouTube(url)
                tit = str(yt.title)

                list_tasks.insert("0",tit)
                progresslabel.config(text="0" + "/" + str(len(links)))
        except:
            clear_input()
            return
        clear_input()
            
    #Se não tiver nada 
    elif target == "":
        print('link sem nada')
        return
    
    #Se for video normal
    else:
        print('é um video normal')
        #Baixa video normal
        try:
            yt = YouTube(target)
            tit = str(yt.title)
            tits.append(tit)
        except:
            clear_input()
            return
        clear_input()
        links.append(target)
        list_tasks.insert("0",tit)
        progresslabel.config(text="0" + "/" + str(len(links)))

def clear_input(Event=None):
    linkText.delete(0,"end")
    
def reset_task_list(Event=None):
    global atual,links,tits

    atual = 0
    links = []
    tits = []
    list_tasks.delete(0, END)
    pb['value'] = 0
    progresslabel.config(text="")
        
def Browse():
    download_Directory = filedialog.askdirectory(initialdir="YOUR DIRECTORY PATH") 
    download_Path.set(download_Directory)
    
def Download():
    global atual
    
    total = 100
    download_Folder = download_Path.get()
    progresslabel.config(text=". . .")
    
    try:
        if links:
            for Youtube_link in links:
                  
                yt = YouTube(Youtube_link)
                
                video = yt.streams.filter(only_audio=True).first()
                out_file = video.download(output_path=download_Folder)

                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                old_file = base + '.mp4'

                try:
                    os.rename(out_file, new_file)
                    
                except:
                    if os.path.exists(new_file):
                        resposta = messagebox.askyesno("YouLey","Já existe alguma dessas músicas, deseja baixar novamente?")
                        if not resposta:
                            os.remove(old_file)
                        else:
                            os.remove(new_file)
                            os.rename(out_file, new_file)
                            
                atual = atual + 1
                progresslabel.config(text=str(atual) + "/" + str(len(links)))
                pb['value'] += total/len(links)
                
            messagebox.showinfo("YouLey","Prontinho!")
        else:
            messagebox.showinfo("YouLey","Quer baixar o que se não tem nada?")   
    except:
        messagebox.showinfo("YouLey","Vixe, deu ruim!")
                
    reset_task_list()
    
root = tk.Tk()

#width = int(465)
#height = int(100)

width = int(435)
height = int(310)

root.geometry(f"{width}x{height}") 
root.resizable(False, False) 
root.title("YouLey") 
root.config(background="white") 
#root.attributes('-alpha',0.85)

downloadPathInitial = str(Path.home() / "Downloads")
downloads_path = downloadPathInitial
download_Path = StringVar() 

#PROGRESS BAR
pb = ttk.Progressbar(root,orient='horizontal',mode='determinate',length=300)
pb.grid(row=22,column=0, columnspan=3, pady=5)

#LABEL DO LINK COPIADO
link_label = Label(root,text="Link copiado :",bg="#E8D579") 
link_label.grid(row=1,column=0,pady=5,padx=5)

#LIST BOX
list_tasks = tk.Listbox(root,justify="center",width=70,height=10,bd=2, fg="green")
list_tasks.grid(row=3, column=0, rowspan=10, columnspan=3, pady=5)
list_tasks.bind("<Delete>", reset_task_list)

#ENTRY DO LINK
linkText = Entry(root,width=55) 
linkText.grid(row=1,column=1,pady=5,padx=5,columnspan = 2)
linkText.bind("<Return>", startThreadProcessToAdd)
linkText.focus()

#DIRETÓRIO A SER SELECIONADO LABEL
destination_label = Label(root,text="Salvar em :",bg="white") 
destination_label.grid(row=2,column=0,pady=5,padx=5) 

#DIRETÓRIO A SER SELECIONADO ENTRY
destinationText = Entry(root,width=40,textvariable=download_Path) 
destinationText.grid(row=2,column=1,pady=5,padx=5)
download_Path.set(downloadPathInitial)
destinationText.configure(foreground="gray")

#BUTÃO PROCURAR
browse_B = Button(root,text="Procurar",command=Browse,width=8,bg="white") 
browse_B.grid(row=2,column=2,pady=1,padx=1) 

#BUTÃO BAIXAR TUDO
Download_B = Button(root,text="Baixar tudo",command=startThreadProcess,width=20,bg="#E8D579") 
Download_B.grid(row=24,column=0,columnspan=4,pady=3,padx=3)

#LABEL PROGRESS
progresslabel = tk.Label(root, text='',width=5, bg="white")
progresslabel.grid(row=22,column=0)

#LABEL FOOTER
footer = tk.Label(root, text='@derleymad',width=10, bg="white")
footer.grid(row=24, column=2,columnspan=2,pady=10)
footer.configure(foreground="gray")

#MAIN LOOP
root.mainloop() 
