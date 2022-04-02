from fileinput import filename
from pytube import YouTube 
import time
import os

links = []

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
        musica = video.download("musicas", filename=f'{tit}.mp3')
    clearConsole() 
    print("\nBaixou tudo com Sucesso\n")

    print('--------------------------\n' + 'Feito com s2 por derleymad' + '\n--------------------------')
    time.sleep(2)

except:
    print("\nAlguma coisa deu errado")
