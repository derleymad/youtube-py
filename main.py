from pytube import YouTube
import moviepy.editor as mp
from alive_progress import alive_bar
import os, time

nlinks = 0
with open("links.txt") as file:
    for url in file:
        nlinks += 1

with alive_bar(nlinks) as bar:
    with open("links.txt") as file:
         for url in file:
             title = 'mp3Download'
             video = YouTube(url).streams.get_audio_only()
             titname = str(video.title)
             video.download("musicas", filename=f'{titname}.mp4')

             time.sleep(0.5)
             clip = mp.AudioFileClip(rf"musicas/{titname}.mp4")
             time.sleep(0.5)
             clip.write_audiofile(rf"musicas/{titname}.mp3", verbose=False, logger='none')
             os.remove(rf"musicas/{titname}.mp4")
             bar()



