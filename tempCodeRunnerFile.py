import speech_recognition as sr
import webbrowser
import pyttsx3
import requests
from gtts import gTTS
import pygame
import os
from youtube_search import YoutubeSearch  # pip install youtube-search-python
import wikipedia  # pip install wikipedia
import datetime
import subprocess
import threading
import time

# -----------------------------------
# Voice Assistant (Jarvis) Project
# -----------------------------------

# Initialize recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Your free News API key (https://newsapi.org)
newsapi = "7eae0d6e46c64d56bd161d9fa6627e11"

# OpenWeather API key (get from https://openweathermap.org/api)
weather_key = "51f37b30c5363143eb0f00180b780513"

# Store alarms
alarms = []


# -------------------------------
# SPEAK FUNCTIONS
# -------------------------------
def speak_old(text):
    """Uses pyttsx3 (offline TTS) to speak."""
    engine.say(text)
    engine.runAndWait()


def speak(text):
    """Uses gTTS (Google TTS) + pygame to speak."""
    try:
        tts = gTTS(text)
        tts.save('temp.mp3')

        pygame.mixer.init()
        pygame.mixer.music.load('temp.mp3')
        pygame.mixer.music.play()

        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)

        pygame.mixer.music.unload()
        os.remove("temp.mp3")
    except Exception as e:
        # fallback to pyttsx3 if gTTS/pygame fails
        print("gTTS/pygame error:", e)
        speak_old(text)


# -------------------------------
# ALARM FUNCTIONS
# -------------------------------
def play_alarm():
    try:
        pygame.mixer.init()
        
        # Full path to your song
        song_path = r"C:\Users\HP\Downloads\Good Morning Song.mp3"
        
        if not os.path.exists(song_path):
            print(f"Song not found: {song_path}")
            return
        
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
    except Exception as e:
        print("Alarm error:", e)
        speak_old("Alarm ringing!")


def alarm_checker():
    while True:
        now = datetime.datetime.now().strftime("%I:%M %p")  # 12-hour format
        if now in alarms:
            print(f"⏰ Alarm ringing for {now}")
            speak("Wake up! Alarm ringing.")
            play_alarm()
            alarms.remove(now)  # remove after ringing
        time.sleep(30)  # check every 30 seconds


# -------------------------------
# AI PROCESS (SIMPLE LOGIC)
# -------------------------------
def aiProcess(command):
    """Basic offline responses (can extend with AI APIs)."""
    if "your name" in command.lower():
        return "I am Jarvis, your personal assistant."
    elif "how are you" in command.lower():
        return "I am fine. Thanks for asking."
    else:
        return "Sorry, I cannot understand that yet without internet AI."


# -------------------------------
# HELPERS
# -------------------------------
def fetch_weather(city="Delhi"):
    """Return a short weather string or None on failure."""
    if not weather_key or "<" in weather_key:
        return None
    try:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={weather_key}&units=metric"
        r = requests.get(url, timeout=8)
        if r.status_code == 200:
            d = r.json()
            main = d.get("main", {})
            weather = d.get("weather", [{}])[0].get("description", "")
            temp = main.get("temp")
            if temp is not None:
                return f"The weather in {city} is {weather} with temperature {temp} degree Celsius."
        return None
    except Exception as e:
        print("Weather error:", e)
        return None


def save_reminder(text):
    with open("reminders.txt", "a", encoding="utf-8") as f:
        f.write(text.strip() + "\n")


def read_reminders():
    if not os.path.exists("reminders.txt"):
        return []
    with open("reminders.txt", "r", encoding="utf-8") as f:
        lines = [ln.strip() for ln in f.readlines() if ln.strip()]
    return lines


# -------------------------------
# PROCESS COMMANDS
# -------------------------------
def processCommand(c):
    """Executes commands based on user input."""
    cl = c.lower()

    # -------------------------------
    # Open websites
    # -------------------------------
    if "open google" in cl:
        webbrowser.open("https://google.com")

    elif "open facebook" in cl:
        webbrowser.open("https://facebook.com")

    elif "open youtube" in cl:
        webbrowser.open("https://youtube.com")

    elif "open linkedin" in cl:
        webbrowser.open("https://linkedin.com")

    # -------------------------------
    # Play song on YouTube
    # -------------------------------
    elif cl.startswith("play"):
        song = cl.replace("play", "").strip()
        try:
            results = YoutubeSearch(song, max_results=1).to_dict()
            if results:
                url = "https://www.youtube.com" + results[0]['url_suffix']
                webbrowser.open(url)
                speak(f"Playing {song} on YouTube")
            else:
                speak("Sorry, I could not find that song.")
        except Exception as e:
            print("YouTube search error:", e)
            speak("Sorry, I could not search YouTube right now.")

    # -------------------------------
    # News
    # -------------------------------
    elif "news" in cl:
        categories = ["business", "entertainment", "general",
                      "health", "science", "sports", "technology"]

        selected_category = None
        for cat in categories:
            if f"{cat} news" in cl or cat in cl and "news" in cl:
                selected_category = cat
                break

        if selected_category:
            url = f"https://newsapi.org/v2/top-headlines?country=in&category={selected_category}&apiKey={newsapi}"
        else:
            url = f"https://newsapi.org/v2/top-headlines?country=in&apiKey={newsapi}"

        try:
            r = requests.get(url, timeout=8)
            articles = []
            if r.status_code == 200:
                data = r.json()
                articles = data.get('articles', [])

            if not articles:
                if selected_category:
                    url2 = f"https://newsapi.org/v2/top-headlines?country=us&category={selected_category}&apiKey={newsapi}"
                else:
                    url2 = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
                r2 = requests.get(url2, timeout=8)
                if r2.status_code == 200:
                    data2 = r2.json()
                    articles = data2.get('articles', [])

            if not articles:
                speak("Sorry, I could not find any news right now.")
            else:
                if selected_category:
                    speak(f"Here are the top {selected_category} news headlines.")
                else:
                    speak("Here are the top news headlines.")
                for idx, article in enumerate(articles[:3], start=1):
                    headline = article.get("title")
                    source = article.get("source", {}).get("name", "Unknown source")
                    if headline:
                        line = f"News {idx}: {headline}, from {source}."
                        print(line)
                        speak(line)
        except Exception as e:
            print("News fetch error:", e)
            speak("Sorry, I could not fetch news right now.")

    # -------------------------------
    # Wikipedia
    # -------------------------------
    elif "search" in cl:
        topic = cl.replace("search", "").strip()
        if not topic:
            speak("What do you want me to search on Wikipedia?")
            return
        try:
            summary = wikipedia.summary(topic, sentences=2, auto_suggest=True, redirect=True)
            print(f"Result for '{topic}':\n{summary}\n")
            speak(summary)

        except wikipedia.exceptions.DisambiguationError as e:
            option = e.options[0]
            summary = wikipedia.summary(option, sentences=2)
            print(f"Result for '{option}':\n{summary}\n")
            speak(summary)

        except wikipedia.exceptions.PageError:
            results = wikipedia.search(topic)
            if results:
                chosen = results[0]
                summary = wikipedia.summary(chosen, sentences=2)
                print(f"Result for '{chosen}':\n{summary}\n")
                speak(summary)
            else:
                print("Sorry, no results found.")
                speak("Sorry, I could not find information on that topic.")

    # -------------------------------
    # Weather
    # -------------------------------
    elif "weather" in cl:
        city = cl.split("weather", 1)[1].strip()
        if city.lower().startswith("in "):
            city = city[3:].strip()

        if not city:
            speak("Please tell me the city name")
        else:
            report = fetch_weather(city=city)
            if report:
                print(report)
                speak(report)
            else:
                speak("Sorry, I could not fetch weather details. Make sure you set your OpenWeather API key.")

    # -------------------------------
    # Reminders
    # -------------------------------
    elif "remind me" in cl:
        reminder_text = cl.replace("remind me", "").strip()
        if not reminder_text:
            speak("What should I remind you about?")
            return
        save_reminder(reminder_text)
        speak(f"Reminder noted: {reminder_text}")

    elif "show reminders" in cl or "list reminders" in cl:
        reminders = read_reminders()
        if not reminders:
            speak("You have no reminders saved.")
        else:
            speak("Here are your reminders.")
            for r in reminders:
                speak(r)

    # -------------------------------
    # System Control
    # -------------------------------
    elif "open notepad" in cl:
        try:
            subprocess.Popen(["notepad.exe"])
            speak("Opening Notepad.")
        except Exception as e:
            print("Notepad error:", e)
            speak("Could not open Notepad.")

    elif "open calculator" in cl:
        try:
            subprocess.Popen(["calc.exe"])
            speak("Opening Calculator.")
        except Exception as e:
            print("Calculator error:", e)
            speak("Could not open Calculator.")

    elif "open vscode" in cl or "open code" in cl or "open vs code" in cl or "open visual code" in cl:
        try:
            subprocess.Popen("code", shell=True)
            speak("Opening Visual Studio Code.")
        except Exception as e:
            print("VSCode error:", e)
            speak("Could not open Visual Studio Code.")

    # -------------------------------
    # Alarm
    # -------------------------------
    elif "set alarm at" in cl:
        time_str = cl.replace("set alarm at", "").strip().lower()

        # Normalize "a.m." / "p.m." to "am" / "pm"
        time_str = time_str.replace(".", "")
        time_str = time_str.replace("am", " AM").replace("pm", " PM")

        alarm_time = None

        try:
        # Try 12-hour format first (e.g., "2:18 PM")
         alarm_time = datetime.datetime.strptime(time_str, "%I:%M %p")
        except ValueError:
            try:
                # Try 24-hour format (e.g., "14:18")
                alarm_time = datetime.datetime.strptime(time_str, "%H:%M")
            except ValueError:
                alarm_time = None

        if alarm_time:
            alarm_str = alarm_time.strftime("%I:%M %p")   # Convert to string
            alarms.append(alarm_str)
            speak(f"Alarm set for {alarm_time.strftime('%I:%M %p')}")
        else:
            speak("Sorry, I could not understand the alarm time. Please say something like 'set alarm at 2:30 PM' or 'set alarm at 14:30'.")
        


    # -------------------------------
    # Default
    # -------------------------------
    else:
        output = aiProcess(c)
        speak(output)


# -------------------------------
# MAIN PROGRAM LOOP
# -------------------------------
if __name__ == "__main__":
    speak("Initializing Jarvis....")

    alarm_thread = threading.Thread(target=alarm_checker, daemon=True)
    alarm_thread.start()

    while True:
        r = sr.Recognizer()
        print("Recognizing...")

        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)

            word = r.recognize_google(audio)

            if word.lower() == "jarvis":
                speak("Ya")
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source, phrase_time_limit=6)
                    command = r.recognize_google(audio)
                    print("Heard:", command)
                    processCommand(command)

        except Exception as e:
            print("Error:", e)
