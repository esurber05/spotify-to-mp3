from flask import Blueprint, redirect, request, session, render_template
from ..utils.spotify import create_spotify_oauth, get_token, gather_playlist_data
import spotipy

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    """Route that sends user to Spotify auth webpage
    
    Gathers URL from Spotify Oauth object and redirects user

    Returns:
        REDIRCT: Spotify app authorization URL
    """
    
    sp_oauth = create_spotify_oauth()
    auth_url = sp_oauth.get_authorize_url()
    
    return redirect(auth_url)

@auth.route('/callback')
def callback():
    """Route from successful Spotify login

    Returns:
        REDIRECT: /selectPlaylist route
    """
    
    sp_auth = create_spotify_oauth()
    session.clear()
    
    #Sets token info for user session
    code = request.args.get('code')
    token_info = sp_auth.get_access_token(code)
    session["token_info"] = token_info
    
    return redirect('/selectPlaylist')

@auth.route('/selectPlaylist')
def selectPlaylist():
    """Route that allows user to select one of their spotify playlists to download

    Returns:
        HTML: 'selectplaylist.html'
        playlists: list of playlist names to be displayed
    """
    
    
    #Validates user token
    try:
        token_info = get_token()
    except:
        return redirect('/')
    
    sp = spotipy.Spotify(auth=token_info['access_token'])
    playlist_data = sp.current_user_playlists()["items"]
    
    #Gets and stores playlist data in session 
    playlist_names, playlist_links = gather_playlist_data(playlist_data)
    session['PLAYLIST_DATA'] = dict(zip(playlist_names, playlist_links))
    
    return render_template('selectplaylist.html', playlists=playlist_names)
