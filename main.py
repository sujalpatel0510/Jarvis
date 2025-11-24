import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import tseries_data
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os
import subprocess
from tseries_data import app_mapping
# pip install pocketsphinx
#git test
recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "b09926aa379c4554869e6332cea79047"

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

# def aiProcess(command):
#     client = OpenAI(api_key="sk-6f5667fb5e024b3ab06c6c1acd19216b",
#     )
#
#     completion = client.chat.completions.create(
#     model="gpt-3.5-turbo",
#     messages=[
#         {"role": "system", "content": "You are a virtual assistant named jarvis skilled in general tasks like Alexa and Google Cloud. Give short responses please"},
#         {"role": "user", "content": command}
#     ]
#     )
#
#     return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    # elif "open youtube" in c.lower():
    #     webbrowser.open("https://youtube.com")
    # elif "open linkedin" in c.lower():
    #     webbrowser.open("https://linkedin.com")
    elif "open chatgpt" in c.lower():
        webbrowser.open("https://chatgpt.com/")
    elif "open deepseek" in c.lower():
        webbrowser.open("https://chat.deepseek.com/")
    elif "open college" in c.lower():
        webbrowser.open("https://www.mbit.edu.in/?page_id=2804")
    elif "open instagram" in c.lower():
        webbrowser.open("https://www.instagram.com/")
    elif "open amazon" in c.lower():
        webbrowser.open("https://www.amazon.in/")
    # elif "open whatsapp" in c.lower():
    #     webbrowser.open("https://web.whatsapp.com/")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)

    elif "tell me news" in c.lower():
        r = requests.get(f"https://newsapi.org/v2/top-headlines?country=in&apiKey=b09926aa379c4554869e6332cea79047")
        if r.status_code == 200:
            # Parse the JSON response
            data = r.json()
            
            # Extract the articles
            articles = data.get('articles', [])
            
            # Print the headlines
            for article in articles:
                speak(article['title'])

    # else:
    #     # Let OpenAI handle the request
    #     output = aiProcess(c)
    #     speak(output)

    if command.startswith("open "):
        app_to_open = command[5:].strip()  # Remove "open " from command
        return open_application(app_to_open)
    return "Command not recognized"


def open_application(app_name):
    """Your existing function modified for app opening"""
    app_name = app_name.lower()

    # Check if app exists in dictionary
    if app_name in app_mapping:
        try:
            # Handle both string paths and dictionary entries
            path = app_mapping[app_name]
            if isinstance(path, dict):
                path = path["path"]

            # Open the application
            if os.path.exists(path):
                subprocess.Popen(path)
            else:
                # Try to open as command if path doesn't exist
                subprocess.Popen(path, shell=True)

            return f"Opening {app_name}"
        except Exception as e:
            return f"Error opening {app_name}: {str(e)}"
    else:
        return f"Application '{app_name}' not found in my database"





if __name__ == "__main__":
    speak("Hello....")
    r = sr.Recognizer()  # create single recognizer to reuse

    try:
        while True:
            # Listen for the wake word "Jarvis"
            print("recognizing...")
            try:
                # Use microphone and adapt to ambient noise first
                with sr.Microphone(device_index=2) as source:   # try built-in mic first
                    # Calibrate for ambient noise (short duration)
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print("Listening for wake word... (say 'Jarvis')")
                    try:
                        audio = r.listen(source, timeout=5, phrase_time_limit=3)
                    except sr.WaitTimeoutError:
                        # No speech within timeout — restart loop
                        print("No speech detected while waiting for wake word.")
                        continue

                # try to recognize the wake word
                try:
                    word = r.recognize_google(audio)
                    print("Heard (wake):", word)
                except sr.UnknownValueError:
                    # Speech was unintelligible
                    print("Couldn't understand wake word audio.")
                    continue
                except sr.RequestError as e:
                    print("Speech recognition service error:", e)
                    continue

                # If wake word matched, listen for the command
                if word.strip().lower() == "jarvis":
                    speak("Yes?")
                    with sr.Microphone(device_index=2) as source:
                        r.adjust_for_ambient_noise(source, duration=0.3)
                        print("Jarvis Active... listening for command")
                        try:
                            audio_cmd = r.listen(source, timeout=6, phrase_time_limit=8)
                        except sr.WaitTimeoutError:
                            print("No command heard, going back to wake-listen.")
                            continue

                    try:
                        command = r.recognize_google(audio_cmd)
                        print("Command:", command)
                        # Process command (use your existing function)
                        processCommand(command)
                    except sr.UnknownValueError:
                        print("Couldn't understand the command.")
                        speak("Sorry, I didn't catch that.")
                        continue
                    except sr.RequestError as e:
                        print("Speech service error:", e)
                        speak("Speech service error.")
                        continue

            except KeyboardInterrupt:
                print("Interrupted by user. Exiting.")
                break
            except Exception as e:
                # Catch-all so your program won't crash quietly
                print("Error:", e)
                # small delay to avoid tight error loop
                import time
                time.sleep(0.5)
                continue

    finally:
        # Clean up resources if needed
        try:
            pygame.mixer.quit()
        except Exception:
            pass
        print("Program ended.")
