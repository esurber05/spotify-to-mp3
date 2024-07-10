var socket = io.connect('http://' + document.domain + ':' + location.port + '/download');
var tracks_completed = -1;

socket.on('connect', function() {
    console.log('Connected to server');
});

socket.on('track-download_progress', function(data) {
    console.log('Progress update received:', data);
    document.getElementById('track-progress-bar').value = data.percent;
    document.getElementById('track-progress-text').innerText = data.percent + "%";
    document.getElementById('track-speed-text').innerText = data.speed;
});

socket.on('track-completed-update', function(data) {
    tracks_completed = tracks_completed + 1;
    document.getElementById('tracks-completed-text').innerText = tracks_completed;
    document.getElementById("current-track-download-text").innerText = data.track_name;
});

socket.on('send-total-tracks', function(data) {
    document.getElementById('total-tracks-text').innerText = data.track_total;
});

socket.on('redirect', function(data) {
    console.log('Redirect:', data);
    window.location.href = data.url;
});

socket.on('disconnect', function() {
    console.log('Disconnected from server');
    socket.disconnect(true);
});
