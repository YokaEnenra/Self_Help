// 2. This code loads the IFrame Player API code asynchronously.
var tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
var firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// 3. This function creates an <iframe> (and YouTube player)
//    after the API code downloads.


function onYouTubeIframeAPIReady() {

}

// 4. The API will call this function when the video player is ready.
function onPlayerReady(event) {
    event.target.playVideo();
}

var player;

function destroyPlayer() {
    if (player) {
        player.destroy();
    }

}

function playThisVideo(vidId) {
    player = new YT.Player('player', {
        height: '360',
        width: '640',
        videoId: vidId,
        events: {
            'onReady': onPlayerReady,
        }
    });
}
