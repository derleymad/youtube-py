from asyncio import subprocess
from tkinter import messagebox, filedialog
from pytube import YouTube,Playlist
from pathlib import Path
from tkinter import ttk
import re,os,threading
from tkinter import *
import tkinter as tk
import subprocess
import patoolib


linksNaoBaixados,threads,links,tits,erros,atual = [],[],[],[],0,0

def unzipFFMPEG():
    if not os.path.isfile('ffmpeg/ffmpeg.exe'):
        patoolib.extract_archive("ffmpeg/ffmpeg.rar", outdir="ffmpeg")
    else:
        return


def bToM(number):
    return number / 1000000
    
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
        p = Playlist(target)

        try:
            for url in p.video_urls:
                links.append(str(url))
                yt = YouTube(url)
                tit = str(yt.title)
                list_tasks.insert("0",tit)
                progresslabel.config(text="0" + "/" + str(len(links)))
        except:
            print("erro em adiconar elem na playlist")
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
            print('falta um link válido')
            clear_input()
            return

        clear_input()
        links.append(target)
        list_tasks.insert("0",tit)
        progresslabel.config(text="0" + "/" + str(len(links)))

def clear_input(Event=None):
    linkText.delete(0,"end")
    
def reset_task_list(Event=None):
    global erros,atual,links,tits,linksNaoBaixados;erros=0;atual=0;links=[];tits=[];linksNaoBaixados=[]

    list_tasks.delete(0, END)
    pb['value'] = 0
    progresslabel.config(text="")
        
def Browse():
    download_Directory = filedialog.askdirectory(initialdir=os.getcwd(),
                                                 title="Selecione canto para baixar as músicas")
    download_Path.set(download_Directory)
    
def Download():
    global atual,erros,linksNaoBaixados
    
    download_Folder = download_Path.get()
    progresslabel.config(text=". . .")

    #Se existir algo na lista de links
    if links:
        for Youtube_link in links:
            try:
                yt = YouTube(Youtube_link)
                
                #video = yt.streams.filter(only_audio=True).first()
                video = yt.streams.get_lowest_resolution()
                out_file = video.download(output_path=download_Folder)

                base,ext = os.path.splitext(out_file)
                new_file = base + '.mp3'

                if 'ffmpeg' in os.getcwd():
                    pass
                else:
                    os.chdir('ffmpeg')

                try:
                    sub = subprocess.getstatusoutput(f'ffmpeg -i "{out_file}" "{new_file}" ')
                    os.remove(out_file)
                except:
                    print('algo no subprocesso')

                atual += 1
                progresslabel.config(text=str(atual) + "/" + str(len(links)))
                pb['value'] += 100/len(links)
                
            except:
                if yt.age_restricted:
                    print('idade restrita')
                
                linksNaoBaixados.append(str(yt.title))
                erros += 1; atual += 1 
                print(yt.title + " não será baixado")
                progresslabel.config(text=str(atual) + "/" + str(len(links)))
                pb['value'] += 100/len(links)

    #Senão existir nada na lista
    else:
        messagebox.showinfo("YouLey","Quer baixar o que se não tem nada?")
        return

    if erros>0:
        msg = str('Baixou quase tudo! Com exceção de: ' + str(erros) + ' musicas'+'\n'+'Quais foram?'+'\n'+str(linksNaoBaixados))
        messagebox.showinfo("YouLey",msg)
    else:
        messagebox.showinfo("YouLey","Prontinho! Todas músicas baixadas")

    reset_task_list()

#ROOT 
root = tk.Tk()
width = int(435)
height = int(310)

#TAMANHO DA TELA E TITULOS
root.geometry(f"{width}x{height}") 
root.resizable(0,0) 
root.title("YouLey") 
root.config(background="white") 
#root.attributes('-alpha',0.85)

#PASTA INICIAL PARA BAIXAR
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

#UNZIP FILES
unzipFFMPEG()

#MAIN LOOP
root.mainloop() 
