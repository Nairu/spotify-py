from typing import Dict

class Song():
    def __init__(self, song_dict: dict):
        self.artists = [artist['name'] for artist in song_dict['artists']]
        self.name = song_dict['name']
        self.popularity = song_dict['popularity']
        self.artist_ids = [artist['id'] for artist in song_dict['artists']]
        self.href = song_dict['external_urls']['spotify']

    def to_dict(self) -> dict:
        return { "artists": self.artists, "name": self.name, "popularity": self.popularity, "href": self.href }