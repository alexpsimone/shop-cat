'use-strict';

// From YouTube Developer API example code.
// This code loads the IFrame Player API code asynchronously.
const tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
const firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// From YouTube Developer API example code, modified to accept any video ID.
// This function creates an <iframe> (and YouTube player)
// after the API code downloads.
// const player;
function onYouTubeIframeAPIReady() {
  const player = new YT.Player('player', {
    height: '390',
    width: '640',
    videoId: 'nNPZilyZfGg',
  //   videoId: 'M7lc1UVf-VE',
    events: {
      'onReady': onPlayerReady,
      'onStateChange': onPlayerStateChange
    }
  });
}

// Adapeted from YouTube Developer API example code.
// The API will call this function when the video player is ready.
function onPlayerReady(evt) {
    evt.target.playVideo();
}

// From YouTube Developer API example code.
// The API calls this function when the player's state changes.
// The function indicates that when playing a video (state=1),
// the player should play for six seconds and then stop.
let done = false;
function onPlayerStateChange(evt) {
  if (evt.data == YT.PlayerState.PLAYING && !done) {
    setTimeout(stopVideo, 0);
    done = true;
  }
}
function stopVideo() {
  player.stopVideo();
}