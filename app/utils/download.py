import os, shutil, spotipy, time, yt_dlp, time
from ..config import Config
from .. import socketio
from ..utils.helpers import strip_ansi_codes, create_zip_file


def download_tracks(playlist_link: str, playlist_name: str, token_info: dict, base_url: str, root_path: str):
    """Downloads tracks form provided Spotify playlist

    Uses provided information to download Spotify tracks through the spotipy and yt_dlp modules.
    
    Args:
        playlist_link (str): link to Spotify playlist
        playlist_name (str): Spotify playlist name
        token_info (dict): token info provided from spotify
        base_url (str): URL for flask web application 
        root_path (str): path to root app folder
    """
    sp = spotipy.Spotify(auth=token_info['access_token'])
    
    # Gathers all tracks from playlistLink given
    tracks_response = sp.playlist_tracks(playlist_link)
    tracks = tracks_response["items"]
    while tracks_response["next"]:
        tracks_response = sp.next(tracks_response)
        tracks.extend(tracks_response["items"])
            
    track_search_entries = create_search_queries(tracks)
            
    playlist_file_name = playlist_name.replace(" ", "-") + time.strftime("%Y%m%d-%H%M%S") + "-(MP3)"
    playlist_folder_path = os.path.join(root_path, 'playlist')
    
    if not os.path.exists(playlist_folder_path):
        os.mkdir(playlist_folder_path)
    
    download_path = os.path.join(root_path + '/playlist/' + playlist_file_name)
    os.mkdir(download_path)
    
    #Downloads all tracks       
    parse_search_queries(track_search_entries, tracks, download_path)
    create_zip_file(download_path, download_path + ".zip")
    
    #Removes original playlist folder
    shutil.rmtree(download_path)
    
    #Redirects user to playlist download route  
    downloadURL = f"{base_url}/playlistdownload/{playlist_file_name}.zip"
    socketio.emit('redirect', {'url': downloadURL}, namespace='/download')

def create_search_queries(playlist_tracks: list) -> list:
    """ Takes a list of tracks from a playlist and creates search entries
    
    Combines track name and artists with the phrase "Audio Only Lyrics" to provide to yt-dlp module.
    For example, a song called Self Control by Frank Ocean would produce 
    "Self Control Frank Ocean Audio Only Lyrics"

    Args:
        playlist_tracks (lists): List of tracks provided 

    Returns:
        list: list of search phrases to send to yt_dlp
    """
    
    track_search_entries = []
    
    for track in playlist_tracks:
        track_info = track["track"]
        track_entry = track_info["name"]
        for artist in track_info["artists"]:
            track_entry += " " + artist["name"]
        track_search_entries.append(track_entry + " Audio Only Lyrics")
    
    return track_search_entries

def parse_search_queries(search_queries: list, tracks: list, download_path: str):
    """Goes through each search query and prepares them from download

    Sends each search query and track object to the searchAndDownload function. 
    Emits data to socket-io to send-total-tracks and the track completed 
    
    Args:
        search_queries (list): list of search queries provided from createSearchQueries()
        tracks (list): list of tracks provided from spotifyAPI module 
        download_path (str): path of folder to send tracks to 
    """
    
    #
    socketio.emit('send-total-tracks', {'track_total': len(tracks)}, namespace='/download')
    
    for search_query, track in zip(search_queries, tracks):
        track = track['track']
        socketio.emit('track-completed-update', {'track_name': track['name']}, namespace='/download')
        search_and_download(search_query, track, download_path)

def search_and_download(query, track, download_path):
    """Downloads mp3 files with provided query and track information

    Uses yt_dlp to download first audio search result, with the given options set. 
    Then it saves it to the provided download path 
    
    Args:
        query (_type_): search query to provide to yt_dlp module 
        track (_type_): track object used in naming 
        download_path (_type_): path where track is downloaded 
    """
    
    
    ydl_opts = {
        'default_search': 'ytsearch',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
        'outtmpl': os.path.join(download_path, f"{track['name']}.%(ext)s"),
        'progress_hooks': [print_progress]
    }
    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            #Picks first entry to download with provided options above
            info = ydl.extract_info(query, download=False)
            
            if 'entries' in info:
                audio_url = info['entries'][0]['url']
                ydl.download([audio_url])
            else:
                print("No audio found for query:", query)
    
    except Exception as e:
        print("Error in downloading track")

def print_progress(status):
    """Emits data to socketIO to show download progress on client side 

    Parses through the data sent by the progress_hook in the yt_dlp module 
    and emits it to socketIO to make a visible progress bar
    
    Args:
        status (_type_): Status provided from progress_hook in yt_dlp 
    """
    
    if 'status' in status and status['status'] == 'downloading':
        
        #Processes data provided by yt_dlp progress_hooks
        percent = status['_percent_str'].strip().replace('%', '')
        speed = status['_speed_str'].strip()
        percent_float = float(strip_ansi_codes(percent))
        
        #Sends for display on progress bar
        socketio.emit('track-download_progress', {'percent': percent_float, 'speed': strip_ansi_codes(speed)}, namespace='/download')
        
