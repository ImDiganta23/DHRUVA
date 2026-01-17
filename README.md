# 🧠 Dhruva – An Intelligent Multimodal Voice & Gesture Assistant

Dhruva is a **Python-based intelligent assistant** that combines **speech recognition, text-to-speech, computer vision, gesture recognition, and real-time AI-driven interaction**.
It is designed as an **educational and interactive companion**, capable of responding to voice commands, performing mathematical operations, detecting hand gestures, counting fingers, recognizing faces, and providing useful information like date, time, and weather.

This project demonstrates the practical integration of **AI, Machine Learning concepts, and real-time system design** using industry-relevant libraries.

---

## 🚀 Key Features

### 🎙 Voice Interaction

* Wake-word based interaction using **speech recognition**
* Natural language understanding for commands
* Conversational text-to-speech responses

### 🧮 Intelligent Math Assistant

* Supports arithmetic operations: addition, subtraction, multiplication, division
* Advanced math functions:

  * Square root
  * Power
  * Percentage
  * Factorial
  * Logarithm & Natural Log
  * Trigonometric functions (sin, cos, tan)
* Robust handling of **misheard voice commands** (e.g., *“sign” → “sine”*)

### ✋ Computer Vision & Gesture Recognition

* Real-time **hand tracking** using webcam
* Finger counting (both hands supported)
* Thumb gestures:

  * 👍 Thumbs up → activate assistant
  * 👎 Thumbs down → exit assistant
* Visual hand landmark rendering

### 👤 Face Detection

* Face mesh detection using MediaPipe
* Works simultaneously with finger counting

### 📚 Educational Capabilities

* Recites poems for children
* Alphabet learning mode (A–Z with examples)

### 🌦 Utility Features

* Real-time weather information via API
* Current date and time announcements

---

## 🛠 Tech Stack Used

### Programming Language

* **Python 3**

### Libraries & Frameworks

* **Speech Recognition**: `speech_recognition`
* **Text-to-Speech**: `pyttsx3`
* **Computer Vision**: `OpenCV (cv2)`
* **Hand & Face Tracking**: `MediaPipe`
* **Math & Parsing**: `math`, `re`, `datetime`
* **Multithreading & Concurrency**: `threading`, `queue`
* **API Integration**: `requests`
* **Real-time Processing**: Webcam + microphone input

---

## 🧩 System Architecture (High-Level)

1. **Speech Input** → Voice command captured via microphone
2. **Command Parsing** → NLP-based pattern matching & number extraction
3. **Execution Engine** → Math, CV, or utility tasks
4. **Computer Vision Thread** → Continuous gesture & finger detection
5. **Response Generation** → Spoken output using TTS

---

## ▶️ How to Run the Project

### Prerequisites

* Python 3.8+
* Webcam
* Microphone

### Install Dependencies

```bash
pip install opencv-python mediapipe speechrecognition pyttsx3 requests
```

### Run the Assistant

```bash
python Dhruva.py
```

---

## 💡 Example Commands

* **“Dhruva, what is the sine of 30?”**
* **“Add 25 and 40”**
* **“Square root of 144”**
* **“What’s the weather in Mumbai?”**
* **“Show fingers”**
* **Thumbs up gesture** to activate listening mode

---

## 📌 Why This Project Stands Out

* Demonstrates **real-time multimodal AI interaction**
* Combines **Computer Vision + Speech AI + NLP**
* Clean modular logic suitable for scaling
* Practical use-case for **education & assistive technology**
* Strong example of **applied AI engineering**, not just theory

---

## 🔮 Future Enhancements

* GUI using Tkinter / PyQt
* Deep learning-based gesture classification
* Offline speech recognition
* User profile & personalization
* Deployment on Raspberry Pi or edge devices

---

## 👨‍💻 Author

**Diganta Ghosh**
B.Tech CSE (AI) | AI & Python Developer
Passionate about building intelligent, human-centric AI systems

---


