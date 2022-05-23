import random
from typing import Union

from fastapi import FastAPI, Request
from fastapi.security import OAuth2PasswordBearer
from starlette.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from song import Song
from spotify import SpotifyHandler
from collections import Counter

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
handler = SpotifyHandler()

@app.middleware("http")
async def check_auth(request: Request, call_next):
    # Basically, if we aren't one of the two auth paths, we want to redirect if we are not authenticated.
    # If we are either of the auth paths, or we are authenticated, we just want to forward on the request
    # And return the response.
    if not (request.url.path == "/") \
        and not (request.url.path == "/auth") \
        and not handler.authenticated():
        return RedirectResponse(url='/')
    else:
        response = await call_next(request)
        return response

@app.get("/", response_class=HTMLResponse)
def read_root():
    return f'<h2><a href="{handler.get_auth_url()}">Sign in</a></h2>'

@app.get("/auth")
def auth(code: Union[str, None] = None):
    if handler.authenticate(code):
        return RedirectResponse(url='/home')
    else:
        return {"error": "code cannot be null!"}

@app.get("/home", response_class=HTMLResponse)
def redirect():
    return f'<h2>Hi {handler.get_spotify().me()["display_name"]}</h2>' \
           f'<a href="/playlists">my playlists</a> | ' \
           f'<a href="/currently_playing">currently playing</a> | ' \
		   f'<a href="/current_user">me</a> | ' \
		   f'<a href="/suggest_playlist">suggest</a> | ' \
           f'<a href="/favourite_songs">favourite songs</a> | ' \
           f'<a href="/favourite_genres">favourite genres</a>'

@app.get("/current_user")
def get_current_user():
    return handler.get_spotify().current_user()

@app.get("/playlists")
def get_user_playlists():
    return handler.get_spotify().current_user_playlists()

@app.get("/currently_playing")
def get_currently_playing():
    track = handler.get_spotify().current_user_playing_track()
    if track is not None:
        return { "artists": Song(track['item']) }
    else:
        return { "error": "No track currently playing" }

@app.get("/favourite_songs")
def read_spotipy():
    results = handler.get_spotify().current_user_saved_tracks()
    return [Song(res['track']) for res in results['items']]

@app.get("/favourite_genres")
def get_favourite_genres():
    return Counter(handler.get_favourite_genres()).most_common(100)

@app.get("/suggest_playlist")
def suggest_playlist(limit: Union[int,None] = 20):
    genres = handler.get_favourite_genres()
    genre = random.choice(genres)
    # Do this so that we don't end up breaking.
    genres.remove(genre)
    while len(handler.get_spotify().search(q=f"genre={genre}", limit=limit)['tracks']['items']) == 0:
        if len(genres) == 0:
            return { "error": "could not find any genres with songs!" }
        genre = random.choice(genres)
    return { "genre": genre, "songs": [Song(item).to_dict() for item in handler.get_spotify().search(q=f"genre={genre}", limit=limit)['tracks']['items']] }