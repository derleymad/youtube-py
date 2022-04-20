import sys
from pytube import YouTube
from pytube import Search

s = Search('poker face')

watch= str(s.results[0].video_id)

flink = str(f'https://www.youtube.com/watch?v={watch}')

yt = YouTube(flink)
filter = yt.streams.first().download()

print(yt.title)
print(filter)

            

