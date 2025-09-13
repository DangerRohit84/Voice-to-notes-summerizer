# Voice-to-Notes Summarizer

An interactive **Python desktop application** that helps you quickly convert your voice (or audio files) into text and then **summarize** it into short, clear notes using **Gemini AI**.  
It provides a clean **Tkinter GUI**, real-time recording, and file upload support.

---

## Features

-  **Microphone Recording** – Start/stop audio capture with a single button.  
-  **Audio File Support** – Process `.wav`, `.mp3`, or `.flac` files easily.  
-  **Speech-to-Text** – Accurate transcription using Google Speech Recognition.  
-  **AI Summarization** – Generates concise notes with Gemini AI.  
-  **User-Friendly GUI** – Built with Tkinter, includes mic/stop icons and text display.  
-  **Responsive Performance** – Background threading ensures smooth GUI operation.  
-  **Reusable Code** – Easy to extend (export notes to PDF, integrate other models, etc.).  

---

##  Requirements

Make sure you have **Python 3.9+** installed.  
Install dependencies using:

```bash
pip install SpeechRecognition
pip install google-generativeai
pip install pillow
