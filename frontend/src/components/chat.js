import React, { useState } from "react";
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

  const sendButtonStyle = {
    ...buttonStyle,
    backgroundColor: isSending ? "#a0aec0" : "#38a169",
  };

  // When the user presses and holds the microphone button.
  const handleMicMouseDown = () => {
    setIsRecording(true);
    setShowSendButton(false); // Hide the send button (if visible)
    setTranscription("Recording...");
  };

  // When the user releases the microphone button.
  const handleMicMouseUp = () => {
    setIsRecording(false);
    setIsProcessing(true);
    setTranscription("Processing voice...");

    // Simulate a 2-second processing delay, then update with hard-coded text.
    setTimeout(() => {
      const simulatedText =
        "My name is Jake. I'm male. My current weight is 200 pounds, my height is 6 feet. My goal is to lose 5 pounds in one month. I have a peanut allergy.";
      setTranscription(simulatedText);
      setIsProcessing(false);
      setShowSendButton(true);
    }, 2000);
  };

  // When the user clicks the Send button.
  const handleSendClick = () => {
    setIsSending(true);
    setTranscription("Sending...");
    setShowSendButton(false);

    // Simulate a sending delay of 1 second.
    setTimeout(() => {
      setIsSending(false);
      setSuccess("Text has been sent");

      setTranscription("Text has been sent"); // Updated to show the final status.
    }, 1000);
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
          {/* Hold the record button to share your name, goal, target time, weight,
          and height. After recording, click 'Send,' scroll, select 'Take
          Photo,' and point your camera at your food. */}
        </div>
      </div>

      {/* Input box (textarea) for transcription */}
      <textarea
        style={textAreaStyle}
        rows="4"
        value={transcription}
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

      {/* Send button (visible once the transcription is available) */}
      {showSendButton && (
        <div style={{ textAlign: "center" }}>
          <button
            style={sendButtonStyle}
            onClick={handleSendClick}
            disabled={isSending}
          >
            {isSending ? "Sending..." : "Send"}
          </button>
          {success && <div style={{ color: "green" }}>{success}</div>}
        </div>
      )}
    </div>
  );
};

export default ChatBox;
