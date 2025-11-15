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
    while True:
        # Listen for the wake word "Jarvis"
        # obtain audio from the microphone
        r = sr.Recognizer()
         
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=4, phrase_time_limit=2)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    print(command)

                    processCommand(command)


        except Exception as e:
            print("Error; {0}".format(e))