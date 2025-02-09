import { useRef, useState } from "react";
import "./canvas.css";

const Canvas = ({ videoRef }) => {
  const canvasRef = useRef(null);
  const [base64Image, setBase64Image] = useState([]);
  const [result, setResult] = useState(null);
  const convertCanvasToBase64 = () => {
    const canvas = canvasRef.current;
    const base64Images = canvas.toDataURL("image/jpeg");
    setBase64Image((prev) => [...prev, base64Images]);
    return base64Images;
  };
  const takePicture = () => {
    const canvas = canvasRef.current;
    const context = canvas.getContext("2d");
    if (videoRef.current && videoRef.current.readyState === 4) {
      // Clear the canvas before drawing
      context.clearRect(0, 0, canvas.width, canvas.height);

      // Draw the video on the canvas without mirroring
      context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    }
  };

  const closeCamera = () => {
    const stream = videoRef.current.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach((track) => {
      track.stop();
    });
  };

  const openCamera = () => {
    navigator.mediaDevices
      .getUserMedia({
        video: {
          facingMode: { exact: "environment" },
        },
      })
      .then((stream) => {
        videoRef.current.srcObject = stream;
      })
      .catch((err) => {
        // alert("Please allow camera access");
      });
  };

  async function makeInference(image) {
    setResult(null);
    console.log(image);
    const f = await fetch("https://10.206.61.53:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ image: image }),
    });
    const data = await f.json();
    console.log(data);
    setResult(data.result);
    return data;
  }

  return (
    <div>
      <canvas hidden ref={canvasRef} width="640" height="480" />
      <div className="buttons">
        <button
          onClick={async () => {
            console.log("clicked");
            takePicture();
            await makeInference(convertCanvasToBase64());
          }}
        >
          Take Picture
        </button>
        <button onClick={openCamera}>Open Camera</button>
        <button onClick={closeCamera}>Close Camera</button>
      </div>
      {result !== null && (
        <div className="nutrition-plan">
          {result && (
            <>
              <div className="summary-section">
                <h2>Summary</h2>
                <p>{result}</p>
              </div>
            </>
          )}
        </div>
      )}
    </div>
  );
};

export default Canvas;
