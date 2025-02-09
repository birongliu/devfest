# NutriVoice: "See with AI, Eat with Confidence"

![screenshot](https://github.com/user-attachments/assets/c20a1026-e9e8-4988-bef3-ed4dfc1c8726)


## Inspiration  

The inspiration for NutriVoice stemmed from a crucial question:  
**How can blind individuals easily access nutritional information about their food?**  

Many existing nutrition apps rely heavily on visual interfaces, making them inaccessible to visually impaired users. We aimed to **bridge this gap** by leveraging AI-powered speech and vision technologies, ensuring that **everyone, regardless of ability, can make informed dietary choices.**  

## What It Does  

NutriVoice is an AI-powered nutrition assistant designed to help **blind and visually impaired users** track their daily calorie intake through voice commands and food recognition.  

## Installation & Setup  

Follow these steps to set up and run the project locally.  

### Clone the Repository  
- **git clone https://github.com/birongliu/devfest.git**  

### Navigate to the Project Directory  
- **Frontend:**  
  - **cd frontend**  
- **Backend:**  
  - **cd inference**  

### Install Dependencies  
- **Frontend:**  
  - **npm install**  
- **Backend:**  
  - **pip install -r requirements.txt**  

### Run the Project  
- **Frontend:**  
  - **npm run start**  
- **Backend:**  
  - **python3 app.py**  

---

## Install Python  
- **Install Python on your machine**  

## Set Up Virtual Environment  
- **Windows:**  
  - **python3 -m venv venv**  
- **Linux/MacOS:**  
  - **source venv/bin/activate**  

---


## Tech Stack  

NutriVoice integrates cutting-edge AI technologies to ensure seamless and accurate nutrition tracking:  
  
![Arch-NutriVoice](https://github.com/user-attachments/assets/9d226556-1610-49ce-9a43-8a7c575aa1b3)

The app allows users to:  
- **Set personal dietary goals** based on weight, height, and timeframe.  
- **Scan food items** using their phone's camera.  
- **Receive instant calorie estimations** via AI-powered food recognition.  
- **Use voice commands** for seamless interaction.  
- **Track daily calorie intake** to stay on course with their nutrition goals.  


## Challenges We Ran Into  

Building NutriVoice was not without its hurdles:  

- **AI Accuracy** – Ensuring precise food recognition and calorie estimations required extensive testing and prompt engineering refinements.  
- **Speech Processing Latency** – Optimizing Whisper API’s response time to provide **real-time feedback** was challenging.  
- **Data Constraints** – Some food items lacked well-documented calorie data, requiring integration with multiple nutrition databases.  
- **User Accessibility Testing** – Designing a voice-first experience for visually impaired users required iterative testing and feedback.  

## Accomplishments That We're Proud Of  

- **Developing a fully functional AI-powered nutrition assistant.**  
- **Achieving high accuracy** in food recognition and calorie estimation.  
- **Creating an intuitive voice-first experience** that makes nutrition tracking accessible to visually impaired users.  
- **Successfully integrating speech recognition** for seamless hands-free operation.  

## What We Learned  

Throughout the development of NutriVoice, we gained valuable insights:  

- **Accessibility must be at the core of design** – Optimizing all features for voice-based interactions was essential.  
- **AI models require continuous improvement** – Fine-tuning food recognition and calorie estimation models was a major learning curve.  
- **User experience matters** – Refining speech-to-text interactions to minimize errors and enhance usability was crucial.  

## What's Next for NutriVoice  

NutriVoice is just the beginning! Future plans include:  

- **Personalized meal recommendations** based on dietary preferences.  
- **Multi-language support** to make the app accessible worldwide.  
- **Crowdsourced food database expansion** to improve accuracy and include more local cuisines.  
- **Offline functionality** to allow users to track nutrition without an internet connection.  

With NutriVoice, we aim to **redefine nutrition accessibility** and empower individuals to take control of their health through AI-driven innovation.  
