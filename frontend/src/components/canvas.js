import { useEffect, useRef, useState } from "react";

const Canvas = ({ videoRef }) => {
  const canvasRef = useRef(null);
  const [base64Image, setBase64Image] = useState([]);

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
      context.drawImage(videoRef.current, 0, 0, canvas.width, canvas.height);
    }
  };

  const closeCamera = () => {
    const stream = videoRef.current.srcObject;
    const tracks = stream.getTracks();
    tracks.forEach((track) => {
      track.stop();
    });
  }

  const openCamera = () => {
    navigator.mediaDevices
      .getUserMedia({
        video: {
          facingMode: "environment"
        },
      })
      .then((stream) => {
        videoRef.current.srcObject = stream;
      })
      .catch((err) => {
        // alert("Please allow camera access");
      });
  }

  async function makeInference(image) {
    console.log(image)
    const f = await fetch("https://10.206.61.53:5000/predict", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ image: image }),
    })
    const data = await f.json();
    console.log(data);
    return data;
  }

  return (
    <div>
      <canvas hidden ref={canvasRef} width="640" height="480" />
      <button onClick={async () => {
        console.log("clicked");
        takePicture();
        await makeInference(convertCanvasToBase64());
      }}>Take Picture</button>
      <button onClick={openCamera}>Open Camera</button>
      <button onClick={closeCamera}>Close Camera</button>
      {console.log(base64Image)}
      {base64Image.map((image, index) => (
        <img key={index} src={image} alt="captured" />
      ))}
    </div>
  );
};

export default Canvas;

