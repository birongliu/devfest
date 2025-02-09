import React, { useEffect, useRef, useState } from "react";
import "./App.css";
import Canvas from "./components/canvas";
import ChatBox from "./components/chat";

function App() {
  const [video, setVideo] = useState(null);
  const videoRef = useRef(null);
  const [isCameraActive, setIsCameraActive] = useState(false);

  const initalizeCamera = () => {
    navigator.mediaDevices
      .getUserMedia({
        video: {
          facingMode: "environment",
        },
      })
      .then((stream) => {
        setVideo(stream);
        setIsCameraActive(true);
      })
      .catch((err) => {
        alert("Please allow camera access");
      });
  };

  const closeCamera = () => {
    if (video) {
      video.getTracks().forEach((track) => track.stop());
      setVideo(null);
      setIsCameraActive(false);
    }
  };

  useEffect(() => {
    if (video === null && !isCameraActive) {
      initalizeCamera();
    } else if (videoRef.current) {
      videoRef.current.srcObject = video;
    }
  }, [video, isCameraActive]);

  return (
    <div className="App">
      <div className="App-header">
        <ChatBox />
        <div className="camera-container">
          {video !== null && (
            <div className="video-container">
              <video autoPlay controls={false} playsInline ref={videoRef} />
              <Canvas videoRef={videoRef} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
