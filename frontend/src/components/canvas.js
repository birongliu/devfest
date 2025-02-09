import { useEffect, useRef, useState } from "react";
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
          {
            result && <>
              <div className="summary-section">
                <h2>Current Status</h2>
                <div className="stats">
                  <p>BMI: {result.summary.current_stats.BMI}</p>
                  <p>
                    Health Status: {result.summary.current_stats.health_status}
                  </p>
                </div>
                <p className="goal">{result.summary.goal_analysis}</p>
                <p className="timeframe">{result.summary.timeframe}</p>
              </div>
              <div className="nutrition-section">
                <h2>Nutrition Plan</h2>
                <p className="calories">
                  Daily Calories: {result.nutrition_plan.daily_calories}
                </p>

                <div className="macros">
                  <h3>Macronutrients</h3>
                  <p>Protein: {result.nutrition_plan.macros.protein}g</p>
                  <p>Carbs: {result.nutrition_plan.macros.carbs}g</p>
                  <p>Fats: {result.nutrition_plan.macros.fats}g</p>
                </div>

                <div className="meal-timing">
                  <h3>Meal Timing</h3>
                  {result.nutrition_plan.meal_timing.map((meal, index) => (
                    <p key={index}>{meal}</p>
                  ))}
                </div>

                <div className="recommendations">
                  <h3>Food Recommendations</h3>
                  {result.nutrition_plan.food_recommendations.map(
                    (rec, index) => (
                      <p key={index}>{rec}</p>
                    )
                  )}
                </div>
              </div>
            </>
          }
        </div>
      )}
    </div>
  );
};

export default Canvas;

