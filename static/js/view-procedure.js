'use strict';

// From YouTube Developer API example code.
// This code loads the IFrame Player API code asynchronously.
let tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
let firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

// From YouTube Developer API example code, modified to accept any video ID.
// This function creates an <iframe> (and YouTube player)
// after the API code downloads.

let vidIDs = ['_8JtnUpkP0s', 'G_l3N0jTNIY'];
let player;

function onYouTubeIframeAPIReady () {

  for (let count = 0; count < vidIDs.length; count += 1) {

    console.log(count);
    const vidInput = $(`#vid-ref-${count + 1}`);
    console.log(vidInput);
    const vidID = vidIDs[count];
    console.log(vidID);

    $(vidInput).replaceWith(
    player = new YT.Player(`player-${count + 1}`, {
    height: '195',
    width: '320',
    videoId: vidIDs[count],
    }));
  };

}

$(document).on('load', onYouTubeIframeAPIReady);