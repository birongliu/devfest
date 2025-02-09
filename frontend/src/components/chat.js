import React, { useRef, useState } from "react";
import logo from "./u.png"; // Import the logo image

const ChatBox = () => {
  const [transcription, setTranscription] = useState(""); // The text inside the input box
  const [isRecording, setIsRecording] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);
  const [isSending, setIsSending] = useState(false);
  const [showSendButton, setShowSendButton] = useState(false);
  const [success, setSuccess] = useState("");

  // Inline styles for the component
  const titleStyle2 = {
    textAlign: "center",
    fontSize: "24px",
    fontWeight: "bold",
    marginBottom: "20px",
    color: "#23471b",
    display: "flex",
    alignItems: "center", // Aligns text and image vertically
  };

  const logoStyle = {
    width: "5rem", // Size of the logo
    height: "5rem",
    marginRight: "10px", // Space between logo and title text
  };

  const descriptionStyle = {
    fontSize: "18px",
    color: "#23471b",
    lineHeight: "1.6",
    textAlign: "center",
    marginBottom: "20px",
  };

  const buttonStyle2 = {
    backgroundColor: "#4caf50",
    color: "#23471b",
    padding: "12px 24px",
    borderRadius: "8px",
    fontSize: "16px",
    border: "none",
    transition: "background-color 0.3s ease",
  };

  const buttonHoverStyle = {
    backgroundColor: "#45a049",
  };
  const containerStyle = {
    width: "100%",
    margin: "20px auto",
    padding: "20px",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
    fontFamily: "Arial, sans-serif",
  };

  const titleStyle = {
    textAlign: "center",
    fontSize: "20px",
    fontWeight: "bold",
    marginBottom: "16px",
  };

  const textAreaStyle = {
    width: "100%",
    border: "1px solid #ccc",
    borderRadius: "4px",
    marginBottom: "16px",
    resize: "none",
  };

  const buttonStyle = {
    padding: "10px 20px",
    borderRadius: "20px",
    border: "none",
    cursor: "pointer",
    color: "white",
    fontSize: "16px",
  };

  const micButtonStyle = {
    ...buttonStyle,
    backgroundColor: isRecording ? "#e53e3e" : "#23471b",
  };
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);
  const sendButtonStyle = {
    ...buttonStyle,
    backgroundColor: isSending ? "#a0aec0" : "#38a169",
  };
 const startRecording = async () => {
   try {
     const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
     const mediaRecorder = new MediaRecorder(stream);

     mediaRecorder.ondataavailable = (event) => {
       if (event.data.size > 0) {
         audioChunksRef.current.push(event.data);
       }
     };

     mediaRecorder.onstop = () => {
       const audioBlob = new Blob(audioChunksRef.current, {
         type: "audio/wav",
       });
       audioChunksRef.current = []; // Clear recorded data
       sendToBackend(audioBlob);
     };

     mediaRecorderRef.current = mediaRecorder;
     mediaRecorder.start();
     setIsRecording(true);
   } catch (error) {
     console.error("Error accessing microphone:", error);
   }
 };
   const sendToBackend = async (blob) => {
     const formData = new FormData();
     formData.append("audio", blob, "audio.wav");

     try {
       const response = await fetch(
         "https://10.206.61.53:5000/speech-to-text",
         {
           method: "POST",
           body: formData,
         }
       );
       const data = await response.json();
       console.log("Transcription:", data.transcription);
       setTranscription(data.transcription);
     } catch (error) {
       console.error("Error sending audio:", error);
     }
   };
     const stopRecording = () => {
       if (mediaRecorderRef.current) {
         mediaRecorderRef.current.stop();
         setIsRecording(false);
       }
     };

  // When the user presses and holds the microphone button.
  const handleMicMouseDown = (r) => {
    r.preventDefault();
    setIsRecording(true);
    setShowSendButton(false); // Hide the send button (if visible)
    setTranscription("Recording...");
    startRecording();
  };

  // When the user releases the microphone button.
  const handleMicMouseUp = (r) => {
    r.preventDefault()
    setIsRecording(false);
    setIsProcessing(true);
    setTranscription("Processing voice...");
    stopRecording();

    // Simulate a 2-second processing delay, then update with hard-coded text.
    setTimeout(() => {
      // const simulatedText =
      //   "My name is Jake. I'm male. My current weight is 200 pounds, my height is 6 feet. My goal is to lose 5 pounds in one month. I have a peanut allergy.";
      // setTranscription(simulatedText);
      setIsProcessing(false);
      setShowSendButton(true);
    }, 2000);
  };


  return (
    <div style={containerStyle}>
      <div style={{ padding: "15px" }}>
        <div style={titleStyle2}>
          <img
            src={logo}
            alt="Logo"
            width={100}
            height={100}
            style={logoStyle}
          />
          <div>Welcome to NutriVoice!</div>
        </div>
        <div style={descriptionStyle}>
          Hold the record button to share your name, goal, target time, weight,
          and height. After recording, scroll, select 'Take
          Photo' and point your camera at your food.
        </div>
      </div>

      {/* Input box (textarea) for transcription */}
      <textarea
        style={textAreaStyle}
        rows="4"
        value={transcription}
        readOnly
        onChange={(e) => setTranscription(e.target.value)}
        placeholder="Your transcription will appear here..."
      />

      {/* Microphone button */}
      <div
        style={{ color: "green", textAlign: "center", marginBottom: "16px" }}
      >
        <button
          style={micButtonStyle}
          onMouseDown={handleMicMouseDown}
          onMouseUp={handleMicMouseUp}
          onTouchStart={handleMicMouseDown}
          onTouchEnd={handleMicMouseUp}
        >
          {isRecording ? "Recording..." : "Hold to Record"}
        </button>
      </div>  
    </div>
  );
};

export default ChatBox;
