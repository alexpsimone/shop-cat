'use strict';

// From YouTube Developer API example code.
// This code loads the IFrame Player API code asynchronously.
let tag = document.createElement('script');

tag.src = "https://www.youtube.com/iframe_api";
let firstScriptTag = document.getElementsByTagName('script')[0];
firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);


// From YouTube Developer API example code, heavily modified to extract
// references from the DOM, determine if they're YouTube video IDs, and then
// generating a new YT player for each arbitrary video ID.

// This function creates an <iframe> (and YouTube player)
// after the API code downloads.

let player;
let vidIDs = [];

function onYouTubeIframeAPIReady () {

  const numStepsInput = $('#num-steps');
  console.log(numStepsInput);
  const NUM_STEPS = $(numStepsInput).val();
  console.log(NUM_STEPS);

  for (let count = 1; count <= NUM_STEPS; count += 1) {
    
    console.log(count);
    const vidInput = $(`#vid-ref-${count}`);
    console.log(vidInput);
    const vidID = $(vidInput).val();
    console.log(vidID);

    if (vidID != 'No Ref Provided' & !vidID.includes('https://')) {
      
      vidIDs.push(vidID);
      console.log(`vidIDs: ${vidIDs}`);

      $(vidInput).replaceWith(
      player = new YT.Player(`player-${count}`, {
      height: '390',
      width: '640',
      videoId: vidID,
      }));

    };
  
  }
}




$(document).on('load', onYouTubeIframeAPIReady);