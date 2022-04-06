from fileinput import filename
from pytube import YouTube 
import time
import os

links = []
destination = 'musicas'

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

with open('links.txt') as file:
    for URL in file:
        links.append(URL)

try:
    for link in links:
        yt = YouTube(link)
        tit = str(yt.title)
        
        print('Baixando ' + tit +'...')

        video = yt.streams.filter(only_audio=True).first()
        out_file = video.download(output_path=destination)

        base, ext = os.path.splitext(out_file)
        
        new_file = base + '.mp3'
        old_file = base + '.mp4'

        try:
            os.rename(out_file, new_file)
        except:
            if os.path.exists(new_file):
                print("Oxe, tu já baixou esse ai...")
                os.remove(old_file)
                time.sleep(2)
            
    clearConsole() 
    print("\nBaixou tudo com Sucesso\n")

    print('--------------------------\n' + 'Feito com s2 por derleymad' + '\n--------------------------')
    time.sleep(2)

except:
    print("\nOxe, alguma coisa deu errado")
