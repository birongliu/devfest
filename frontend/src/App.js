import React, { useEffect, useRef } from "react";
import "./App.css";
import Canvas from "./components/canvas";
import ChatBox from "./components/chat";

function App() {
  const [video, setVideo] = React.useState(null);
  const videoRef = useRef(null);

  const initalizeCamera = () => {
    navigator.mediaDevices
      .getUserMedia({
        video: {
         facingMode: "environment"
        },
      })
      .then((stream) => {
        setVideo(stream);
      })
      .catch((err) => {
        // alert("Please allow camera access");
      });
  };

  useEffect(() => {
    if (video === null) {
      initalizeCamera();
    } else if (videoRef.current) {
      videoRef.current.srcObject = video;
    }
  }, [video]);



  return (
    <div className="App">
      <div className="App-header">
        <ChatBox />
        {video !== null && (
          <video autoPlay controls={false} playsInline ref={videoRef} />
        )}
        {video !== null && <Canvas videoRef={videoRef} />}
      </div>
    </div>
  );
}

export default App;
