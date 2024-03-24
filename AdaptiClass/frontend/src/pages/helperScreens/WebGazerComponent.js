import React, {useEffect} from "react";

const WebGazerComponent = ({component: Component}) => {
    useEffect(()=>{
        const webgazer = window.webgazer;
        webgazer.showVideoPreview(true)
        .showVideo(false)
        // .showFaceOverlay(false)
        // .showFaceFeedbackBox(false)
        .showPredictionPoints(true)
        .setGazeListener((data, clock)=> {
          console.log(data, clock);
        }).begin();

        const removeWebgazer = () => {
            webgazer.pause();
            
            setTimeout(() => {

                const gazeDot = document.getElementById("webgazerGazeDot");

                if (gazeDot) {
                    console.log(gazeDot);
                    gazeDot.remove();
                }

                const webgazerVideoContainer = document.querySelectorAll("#webgazerVideoContainer");
                if (webgazerVideoContainer) {
                    webgazerVideoContainer.forEach(container => {
                        const videoElement = container.querySelector('#webgazerVideoFeed');
                        
                        if (videoElement) {
                            const mediaStream = videoElement.srcObject; // Get the media stream from the video element
                            if (mediaStream) {
                                const tracks = mediaStream.getTracks(); // Get all tracks from the media stream
                                tracks.forEach(track => track.stop()); // Stop all tracks
                            }
                            videoElement.srcObject = null; // Clear the source object of the video element
                            videoElement.remove(); // Remove the video element
                        }

                        container.remove();
                        console.log(container);
                    })
                }

            },2000);

            
            

        }

        return () => {
            //document.getElementById("webgazerVideoContainer").remove();
            removeWebgazer();
        };
    },[]);


    return(
        <div>
            <Component />
        </div>
    )
}

export default WebGazerComponent;