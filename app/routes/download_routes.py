from flask import Blueprint, request, render_template, send_file, redirect, session, current_app
import os
from ..utils.download import download_tracks
from ..utils.spotify import get_token
from .. import socketio

download = Blueprint('download', __name__)

@download.route('/download', methods=['POST'])
def download_route():
    """Route for downloading playlist tracks
    
    Gathers required data such which is then sent to socketio 
    to download tracks in the background
    
    POST: handles playlist selection data

    Returns:
        HTML: download.html template
    """
    
    
    #Validates user token and playlist
    try:
        playlist_name = request.form.get("playlist")
        token_info = get_token()    
    except:
        return redirect('/')
    
    #Gathers required data (needs app context)
    base_url = request.host_url.rstrip('/')
    root_path = current_app.root_path
    playlist_data = session.get('PLAYLIST_DATA', {})
    playlist_link = playlist_data.get(playlist_name).split('/')[-2]
    
    socketio.start_background_task(download_tracks, playlist_link, playlist_name, token_info, base_url, root_path)
    
    return render_template("download.html")

@download.route('/playlistdownload/<playlist_file>')
def playlist_download(playlist_file: str):
    """Route handling the template of the file download

    Args:
        playlist_file (str): path to zip file of playlist

    Returns:
        HTML: playlistdownload.html template
        HTML: 404 error 
    """
    file_path = current_app.root_path + '/playlist/' + playlist_file
    
    #Check if path exists if not return error
    if os.path.exists(file_path):
        return render_template('playlistdownload.html', playlist_file=playlist_file)
    else:
        return "File not found", 404

@download.route('/sendfile/<path:file_path>')
def send_playlist(file_path: str):
    """Sends file to user for download

    Sends already validated file path to user when clicked on 
    in the playlistdownload.html
    
    Args:
        filePath (str): path to file

    Returns:
        file: downloaded file
    """
    return send_file(file_path)
