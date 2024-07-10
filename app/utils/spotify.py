from spotipy.oauth2 import SpotifyOAuth
import time
from flask import session, url_for
from ..config import Config

def create_spotify_oauth():
    """Generates spotify oauth object
    
    Uses spotipy module to generate a SpotifyOAuth Object using the client_id and client_secret from web app

    Returns:
        SpotifyOAuth: object allowing access to Spotify user data
    """
    
    
    return SpotifyOAuth(
        client_id=Config.CLIENT_ID,
        client_secret=Config.CLIENT_SECRET,
        redirect_uri=url_for('auth.callback', _external=True),
        scope="user-library-read"
    )

def get_token():
    """Gets access token for Spotify user 
    
    Pulls token info from session, if token is expired gathers a new one

    Returns:
        dict: all token info provided through session data
    """
    
    token_info = session.get("token_info", None)
    
    if not token_info:
        raise "exception"
    
    #Gets new token if expired 
    current_time = int(time.time())
    is_expired = token_info['expires_at'] - current_time < 60
    
    if is_expired:
        sp_auth = create_spotify_oauth()
        token_info = sp_auth.refresh_access_token(token_info['refresh_token'])
    
    return token_info

def gather_playlist_data(playlist_data: dict):
    """Gets all user playlist to be displayed

    Args:
        playlist_data (dict): dictionary provided by spotipy containing all user playlists

    Returns:
        list: two lists, one containing the playlist names the 
        other containing the playlist links
    """
    
    
    playlist_links = []
    playlist_names = []
    
    for playlist in playlist_data:
        playlist_links.append(playlist["tracks"]["href"])
        playlist_names.append(playlist["name"])
    
    return playlist_names, playlist_links
