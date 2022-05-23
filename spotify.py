from typing import Union
import json

from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify

class SpotifyHandler():
    def __init__(self):
        # Try and get the info from the credentials json.
        data = None
        with open('credentials.json') as json_file:
            data = json.load(json_file)

        if data:
            self.auth_manager = SpotifyOAuth(scope=data['scope'],
                                            show_dialog=True,
                                            client_id=data['client_id'],
                                            client_secret=data['client_secret'],
                                            redirect_uri=data['redirect_uri'])
            self.spotify = None
            self.token = None
    
    def authenticated(self):
        # We're authenticated if we have a token and it isn't invalid.
        return self.token is not None and not self.auth_manager.is_token_expired(self.token) and self.spotify is not None

    def authenticate(self, code: Union[str, None] = None):
        self.token = self.auth_manager.get_access_token(code)
        if self.token is not None:
            self.spotify = Spotify(auth_manager=self.auth_manager)
        return self.token is not None and self.spotify is not None

    def get_auth_url(self):
        return self.auth_manager.get_authorize_url()

    def get_spotify(self):
        return self.spotify

    def get_songs_from_playlists(self, playlist_ids):
        ret = []
        for id in playlist_ids:
            playlist_items = self.spotify.playlist_items(id)
            if (len(playlist_items['items']) > 0 and playlist_items['items'][0] is dict): 
                ret.extend(playlist_items)
        return ret

    def get_favourite_genres(self):
        # If we're going to suggest a playlist, we can get info about the top songs, grab one of the genres and then return
        # A playlist made of songs from that playlist.
        # We need to get our songs from a few places:
        # - saved songs
        # - songs in playlists
        # - recently played songs
        results_saved_tracks = self.spotify.current_user_saved_tracks()
        results_recently_played_tracks = self.spotify.current_user_recently_played()
        results_playlists = self.spotify.current_user_playlists(limit=50)

        songs = []
        songs.extend(results_saved_tracks['items'])
        songs.extend(results_recently_played_tracks['items'])
        songs.extend(self.get_songs_from_playlists([playlist['id'] for playlist in results_playlists['items']]))

        artists = []
        for uid in [artist['id'] for song in songs for artist in song['track']['artists']]:
            artists.append(self.spotify.artist(uid))
        return [genre for artist in artists for genre in artist['genres']]