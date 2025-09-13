import tkinter as tk
from tkinter import filedialog
import speech_recognition as sr
import google.generativeai as genai
from PIL import Image, ImageTk
import threading

# ==== Configure Gemini ====
genai.configure(api_key="AIzaSyAfoEvrewret00RVLN-c_wXgvOOI5qO3DY")
model = genai.GenerativeModel("gemini-1.5-flash")

recognizer = sr.Recognizer()
microphone = sr.Microphone()

recording = False
audio_chunks = []

# ==== Summarize with Gemini ====
def summarize_text(text):
    try:
        prompt = f"Summarize this text into clear short notes:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Gemini Error: {e}"

# ==== Recording from mic ====
def record_audio():
    global recording, audio_chunks
    audio_chunks = []
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        text_box.insert(tk.END, "Recording...\n")
        while recording:
            try:
                audio = recognizer.listen(source, timeout=1, phrase_time_limit=None)
                audio_chunks.append(audio)
            except sr.WaitTimeoutError:
                continue
    # Combine chunks after stop
    if audio_chunks:
        combined_audio = audio_chunks[0]
        for chunk in audio_chunks[1:]:
            combined_audio.frame_data += chunk.frame_data
        process_audio(combined_audio)

# ==== Process audio ====
def process_audio(audio):
    try:
        text = recognizer.recognize_google(audio)
        summary = summarize_text(text)
        text_box.delete(1.0, tk.END)
        text_box.insert(tk.END, f"Original:\n{text}\n\n🔎 Summary:\n{summary}")
    except sr.UnknownValueError:
        text_box.insert(tk.END, "Could not understand audio\n")
    except Exception as e:
        text_box.insert(tk.END, f"Error: {e}\n")

# ==== Toggle mic button ====
def toggle_recording():
    global recording
    if not recording:
        recording = True
        mic_button.config(image=stop_photo)
        threading.Thread(target=record_audio, daemon=True).start()
    else:
        recording = False
        mic_button.config(image=mic_photo)
        text_box.insert(tk.END, "Recording stopped.\n")

# ==== Load audio file ====
def load_audio_file():
    file_path = filedialog.askopenfilename(filetypes=[("Audio Files", "*.wav *.mp3 *.flac")])
    if not file_path:
        return
    text_box.insert(tk.END, f"Processing file: {file_path}\n")
    try:
        with sr.AudioFile(file_path) as source:
            audio = recognizer.record(source)
        process_audio(audio)
    except Exception as e:
        text_box.insert(tk.END, f"Error: {e}\n")

# ==== GUI ====
root = tk.Tk()
root.title("Voice-to-Notes Summarizer")
root.geometry("500x500")

# Load images
try:
    mic_img = Image.open("mic.png").resize((60, 60))
    stop_img = Image.open("stop.png").resize((60, 60))
    mic_photo = ImageTk.PhotoImage(mic_img)
    stop_photo = ImageTk.PhotoImage(stop_img)
except:
    mic_photo = None
    stop_photo = None

# Mic toggle button
mic_button = tk.Button(root, image=mic_photo, text="🎤", font=("Arial", 14), command=toggle_recording)
mic_button.pack(pady=10)

# Load audio file button
file_button = tk.Button(root, text="Load Audio File", font=("Arial", 12), command=load_audio_file)
file_button.pack(pady=5)

# Text area
text_box = tk.Text(root, wrap="word", height=20, width=60)
text_box.pack(padx=10, pady=10)

root.mainloop()
