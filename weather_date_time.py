import pyttsx3
import requests
import speech_recognition as sr
import datetime
import time
import pyaudio

# Initialize the text-to-speech engine
engine = pyttsx3.init()
engine.setProperty("rate", 180)
engine.setProperty("volume", 0.9)

def speak(text):
    """Speak the given text using TTS."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice input and return it as text."""
    recognizer = sr.Recognizer()
    recognizer.dynamic_energy_threshold = True
    recognizer.energy_threshold = 300
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=7)
            return recognizer.recognize_google(audio).lower()
        except (sr.UnknownValueError, sr.RequestError, sr.WaitTimeoutError):
            return None

def get_weather(city, api_key):
    """Fetch current weather and forecast for a given city."""
    try:
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": api_key, "units": "metric"}
        response = requests.get(base_url, params=params).json()
        
        if "weather" in response and "main" in response:
            wind_speed = response["wind"]["speed"]
            wind_description = classify_wind_speed(wind_speed)
            
            return {
                "description": response["weather"][0]["description"],
                "temperature": response["main"]["temp"],
                "humidity": response["main"]["humidity"],
                "rain": response.get("rain", {}).get("1h", 0),
                "wind_description": wind_description,
            }
        return None
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return None

def classify_wind_speed(speed):
    """Classify wind speed into descriptive labels."""
    if speed > 10:
        return "strong wind"
    elif 5 < speed <= 10:
        return "mild breeze"
    else:
        return "pleasant breeze"

def generate_forecast_report(weather, city):
    """Generate a summarized weather report."""
    report = (f"In {city}, it's {weather['description']} with a temperature of {weather['temperature']}°C. "
              f"Humidity is at {weather['humidity']}%. The air feels like a {weather['wind_description']}.")
    
    if weather["rain"] > 0:
        report += " Light rain is expected. Don't forget your umbrella!"
    return report

def get_current_datetime():
    """Provide the current date or time."""
    now = datetime.datetime.now()
    return now.strftime("%A, %d %B %Y"), now.strftime("%I:%M %p")

def ask_city_and_get_weather(api_key):
    """Handle the flow of asking for the city and fetching weather."""
    speak("Which city's weather would you like to check?")
    while True:
        city = listen()
        if city:
            weather = get_weather(city, api_key)
            if weather:
                report = generate_forecast_report(weather, city)
                speak(report)
                print(report)
                break
            else:
                speak("I couldn't fetch the weather details for that city. Please try again.")
        else:
            speak("I didn't catch the city name. Could you repeat?")

def main():
    api_key = "6d31c19b9abf5128f624334bdbd92bdd"  # Replace with your OpenWeatherMap API key
    active = False
    speak("Hello, I'm Dhruva, your personal assistant. Call me if you need any help.")
    print("Dhruva is running...")

    while True:
        command = listen()
        if command:
            if "dhruva" in command and not active:
                active = True
                speak("Hi there! I'm listening. What can I do for you?")
            elif "shutdown" in command and active:
                speak("Goodbye! Take care!")
                print("Dhruva shutting down...")
                break
            elif active:
                if "weather" in command:
                    ask_city_and_get_weather(api_key)
                elif "time" in command:
                    _, current_time = get_current_datetime()
                    speak(f"The current time is {current_time}.")
                    print(f"The current time is {current_time}.")
                elif "date" in command:
                    current_date, _ = get_current_datetime()
                    speak(f"Today's date is {current_date}.")
                    print(f"Today's date is {current_date}.")
                else:
                    speak("I'm here to assist you! Let me know how I can help.")
            elif not active:
                print("Waiting for 'Dhruva' activation...")
        else:
            time.sleep(1)  # Delay to avoid looping too rapidly

if __name__ == "__main__":
    main()
