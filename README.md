# Spotify Playlist Downloader

Download your Spotify playlists as MP3 files.

## Purpose

This tool allows users to download tracks from their Spotify playlists directly to their local storage as MP3 files. It simplifies the process of accessing offline versions of your favorite playlists, making it ideal for individuals who want to enjoy their tunes without an internet connection.

## Features

- **OAuth2 Authentication**: Securely login with your Spotify account.
- **Playlist Selection**: Choose which playlist to download.
- **Background Downloading**: Tracks are downloaded in the background.
- **Real-time Progress**: Track the download progress in real-time.

## Installation

1. **Clone the repository**:
    ```bash
    git clone https://github.com/esurber05/spotify-to-mp3
    cd spotify-playlist-downloader
    ```

2. **Set up Python virtual environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Set up config variables**:
    - Create a `config.py` file and add your Spotify API and session information:
        ```env
        CLIENT_ID='your-client-id'
        CLIENT_SECRET='your-client-secret'
        SECRET_KEY='flask-secret-key'
        SESSION_COOKIE_NAME='your-session-cookie-name'
        SESSION_TYPE='filesystem'
        ```

5. **Run the application**:
    ```bash
    flask run
    ```

## Quick Start

1. Navigate to `http://localhost:5000` in your web browser.
2. Log in with your Spotify account.
3. Select a playlist to download.
4. Monitor the download progress and retrieve your MP3 files.

## Libraries Used

- [Flask](https://flask.palletsprojects.com/)
- [Flask-SocketIO](https://flask-socketio.readthedocs.io/)
- [Spotipy](https://spotipy.readthedocs.io/)
- [yt-dlp](https://github.com/yt-dlp/yt-dlp)
- [FFmpeg](https://ffmpeg.org/)

