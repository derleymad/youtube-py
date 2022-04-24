from pytube import YouTube, Playlist
import os, re

class Musica:
    def __init__(self, titulo, link):
        self.titulo = titulo
        self.link = link

    def getTitulo(self):
        return self.titulo

    def getLink(self):
        return self.titulo

class Script:
    def __init__(self,link):
        self.links = [] 
        self.link = link
        self.checkPlaylist()
        self.tamanho = len(self.links) 

    def checkPlaylist(self):
        x = str(re.findall("playlist", self.link))

        if 'playlist' in x:
            print('é uma playlist')
            self.playlist = Playlist(self.link)

            for url in self.playlist.video_urls:
                yt = YouTube(url)
                self.musica = Musica(str(yt.title), str(url))
                self.links.append(self.musica)

    def printTitlesLinks(self):
        for i in self.links:
            print(i.titulo,i.link)