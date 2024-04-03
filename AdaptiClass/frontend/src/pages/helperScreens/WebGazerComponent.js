import React, {useEffect, useState} from "react";
import axios from "axios";

const WebGazerComponent = ({component: Component}) => {

    useEffect(()=>{

        const currentDateTimeString = new Date().toLocaleString('en-US', { timeZone: Intl.DateTimeFormat().resolvedOptions().timeZone });
        const currentDateTimeWithTimeZone = new Date(currentDateTimeString);

        const isInitialized = true;

        const webgazer = window.webgazer;
        var webgazerStartTime = 0;
        var webgazerEndTime = 0;
        var engagedTime = 0;
        var blockState = "engaged";
        var blockStartTime = 0;
        var blocks = [];


        webgazer.showVideoPreview(true)
        .showVideo(false)
        .showPredictionPoints(false)
        .setGazeListener((data, clock)=> {
            
            //Set start time if it hasn't yet been created.
            if (webgazerStartTime === 0) {
                webgazerStartTime = clock;
            }

            webgazerEndTime = clock;

            //If state is changing from an engaged period to a disengaged period
            if (data === null && blockState==="engaged") {
                
                const blockDuration = clock - blockStartTime;

                //Filtering noise - change must have lasted at least 1 second. 
                if (blockDuration > 5000) {
                    blocks.push({ state: "engaged", start: blockStartTime, duration: blockDuration, end: clock })
                    engagedTime += blockDuration;
                    blockState = "disengaged";
                    blockStartTime = clock;
                }
                
            //If state is changing from a disengaged period to an engaged period. 
            } else if (data !== null && blockState==="disengaged") {
                
                const blockDuration = clock - blockStartTime;

                //Filtering noise - change must have lasted at least 1 second. 
                if (blockDuration > 5000) {
                    blocks.push({ state: "disengaged", start: blockStartTime, duration: blockDuration, end: clock })
                    blockState = "engaged";
                    blockStartTime = clock;
                }
            }
            

        }).begin();

        const formatData = (startDatetime, endTime, engagedTime, engagementPeriods) => {

            const dataToSend = {
                "start": startDatetime,
                "end": new Date(startDatetime.getTime() + endTime),
                "total_time": endTime,
                "engaged_time": engagedTime,
                "engagement_periods": engagementPeriods
            };

            return dataToSend;
        }

        const removeWebgazer = () => {
            webgazer.pause();

            
            setTimeout(() => {

                const gazeDot = document.getElementById("webgazerGazeDot");

                if (gazeDot) {
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
                    })
                }

            },2000);

            
            

        }

        const handleDataSubmission = async (engagementData) => {
        
            try {
                const response = await axios.post('http://127.0.0.1:8000/engagementdata/', engagementData);
                console.log(response.data);
            } catch (error) {
                console.error('Error:', error);
            }
        };

        return () => {
            
            removeWebgazer();

            //If the last block is engaged, add its duration to the total engagement time. 
            if (blockState === "engaged"){
                engagedTime += webgazerEndTime-blockStartTime;
            }

            //Add the last block
            blocks.push({ state: blockState, start: blockStartTime, duration: webgazerEndTime-blockStartTime, end: webgazerEndTime })

            handleDataSubmission(formatData(currentDateTimeWithTimeZone, webgazerEndTime, engagedTime, blocks));
            
        };
    },[]);

    return(
        <div>
            <Component />
        </div>
    )
}

export default WebGazerComponent;