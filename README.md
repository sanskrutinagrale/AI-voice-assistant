#  Jarvis – AI Voice Assistant  

Jarvis is a Python-based **voice-controlled AI assistant** that can perform tasks such as fetching news, checking weather, setting alarms, managing reminders, opening applications, and playing YouTube music — all through simple voice commands. Handles small talk with predefined responses.

---

## Tech Stack  

- **Programming Language**: Python  
- **Libraries**:  
  - `speech_recognition` – for speech-to-text  
  - `gTTS` & `pyttsx3` – for text-to-speech  
  - `pygame` – for playing audio  
  - `requests` – for APIs (OpenWeather API & NewsAPI)  
  - `youtube_search` – for finding YouTube music  
  - `wikipedia` – for Wikipedia summaries  
  - `datetime`, `threading`, `subprocess`, `os` – for alarms, reminders, and system tasks  

---

## Installation  

1. Clone the repository:  
   ```bash
   git clone https://github.com/your-username/jarvis-ai-assistant.git
   cd jarvis-ai-assistant
   ```

2. Install dependencies:  
   ```bash
   pip install -r requirements.txt
   ```

3. Add your **API Keys**:  
   - Get a free API key from [NewsAPI](https://newsapi.org) and [OpenWeather](https://openweathermap.org).  
   - Replace them inside the script:  
     ```python
     newsapi = "YOUR_NEWS_API_KEY"
     weather_key = "YOUR_OPENWEATHER_API_KEY"
     ```

4. Run the assistant:  
   ```bash
   python jarvis.py
   ```

---

## Project Structure  

```
 jarvis-ai-assistant
 ┣ 📜 jarvis.py          # Main code file
 ┣ 📜 reminders.txt      # Saved reminders
 ┣ 📜 requirements.txt   # Python dependencies
 ┗ 📜 README.md          # Documentation
``` 
