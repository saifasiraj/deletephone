from menu import *
from mutagen.easyid3 import EasyID3
import os
import pygame


directory = './'
musicdirectory = directory + 'Music/'
playlistdirectory = directory + 'Playlists/'
music = os.listdir(musicdirectory)
playlists = os.listdir(playlistdirectory)
artists = []
albums = []
print(music)


def play(audio):
    pygame.mixer.music.load(music + audio)
    pygame.mixer.music.play(loops=0)


def get_song_title_by_file(file):
    music_data = EasyID3(musicdirectory + file)
    if 'title' in music_data:
        return music_data['title'][0]
    return file

def get_artists():
    global artists
    artists = []
    misc = False
    for f in range(0, len(music)):
        music_data = EasyID3(musicdirectory + music[f])
        print(hasattr(music_data, 'artist'))

        print(music_data)
        if (not ('artist' in music_data)) or len(music_data['artist']) <= 0:
            misc = True
            continue
        artist = music_data['artist'][0]
        if not ((artist in artists) or (artist.lower() in artists)):
            artists.append(artist)

    if misc:
        artists.append('Misc')


def get_albums():
    global albums
    albums = []
    for f in range(0, len(music)):
        music_data = EasyID3(musicdirectory + music[f])
        print(music_data)
        if 'album' in music_data:
            album = music_data['album'][0]
            if not ((album in albums) or (album.lower() in albums)):
                albums.append(album)


def get_songs_by_artist(artist):
    songs = []
    for f in range(0, len(music)):
        music_data = EasyID3(musicdirectory + music[f])
        if artist == 'Misc':
            if (not ('artist' in music_data)) or len(music_data['artist']) <= 0:
                songs.append(music[f])
        else:
            if ('artist' in music_data) and len(music_data['artist']) > 0:
                artist_data = music_data['artist'][0].lower()
                if artist.lower() == artist_data:
                    songs.append(music[f])
    return songs


def get_songs_by_album(album):
    songs = []
    for f in range(0, len(music)):
        music_data = EasyID3(musicdirectory + music[f])
        if ('album' in music_data) and len(music_data['album']) > 0:
            album_data = music_data['album'][0].lower()
            if album.lower() == album_data:
                songs.append(music[f])
    return songs

def get_songs_by_playlist(playlist):
    songs = []
    file = open(playlistdirectory + playlist + '.m3u', "r")
    for song in file:
        songs.append(song.strip())

    file.close()
    return songs

class MusicPage(MenuPage):
    def __init__(self, previous_page):
        super().__init__("Music", previous_page, has_sub_page=True)
        self.pages = [
            SongsPage(self),
            ArtistsPage(self),
            AlbumsPage(self),
            PlaylistsPage(self),
        ]
        self.index = 0
        self.page_start = 0

    def get_pages(self):
        return self.pages

    def total_size(self):
        return len(self.get_pages())

    def page_at(self, index):
        return self.get_pages()[index]


class ArtistsPage(MenuPage):
    def __init__(self, previous_page):
        super().__init__("Artists", previous_page, has_sub_page=True)
        get_artists()
        print(artists)

    def page_at(self, index):
        # play track
        artist = artists[index]
        return SongsPage(self, artist, 'artists')

    def total_size(self):
        return len(artists)


class AlbumsPage(MenuPage):
    def __init__(self, previous_page):
        super().__init__("Albums", previous_page, has_sub_page=True)
        get_albums()

    def page_at(self, index):
        # play track
        album = albums[index]
        return SongsPage(self, album, 'albums')

    def total_size(self):
        return len(albums)


class PlaylistsPage(MenuPage):
    def __init__(self, previous_page):
        super().__init__("Playlists", previous_page, has_sub_page=True)

    def page_at(self, index):
        # play track
        playlist = playlists[index].split('.')
        playlist.pop()
        playlist = '.'.join(playlist)
        return SongsPage(self, playlist, 'playlists')

    def total_size(self):
        return len(playlists)


class Song(MenuPage):
    def __init__(self, previous_page, header, has_sub_page=True, is_title=False):
        super().__init__(header, previous_page, has_sub_page, is_title)


class SongsPage(MenuPage):
    def __init__(self, previous_page, header=None, type='all'):
        self.header = header if header else 'Songs'
        super().__init__(self.header, previous_page, has_sub_page=False)
        if type == 'artists':
            self.songs = get_songs_by_artist(self.header)
        elif type == 'albums':
            self.songs = get_songs_by_album(self.header)
        elif type == 'playlists':
            self.songs = get_songs_by_playlist(self.header)
        else:
            self.songs = music

    def nav_select(self, index=None):
        play(self.songs[self.index])
        return self

    def page_at(self, index):
        return Song(self, get_song_title_by_file(self.songs[index]), False)

    def total_size(self):
        return len(self.songs)

