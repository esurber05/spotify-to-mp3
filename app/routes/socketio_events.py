from .. import socketio
from ..utils.helpers import delete_old_files
import os

@socketio.on('connect', namespace='/download')
def handle_connect():
    """Handles connection to socketIO on /download
    """
    
    print("Client connected")
    socketio.emit('message', {'data': 'Connected to server'}, namespace='/')

@socketio.on('disconnect', namespace='/download')
def handle_disconnect():
    """Handles discnnection to socketIO on /download
    
    Function also causes the playlist folder to be cleared, 
    deleting any files that are older than a day
    """
    
    print("Client disconnected")
    
    # Clears old playlists 
    playlist_folder_path = os.path.join(os.getcwd(), 'app', 'playlist')
    delete_old_files(playlist_folder_path)
