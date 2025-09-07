import threading
import queue
import time
import cv2
import mediapipe as mp
import speech_recognition as sr
import pyttsx3
import random
import math
import datetime
import requests
import re

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# Initialize MediaPipe Hands for gesture recognition
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Wake-up and shutdown flags
active = False
shutdown_flag = False

# Speech Queue
speech_queue = queue.Queue()

# Text-to-speech threading
last_spoken = ""

def tts_worker():
    while True:
        text = speech_queue.get()
        if text == "EXIT":
            break
        engine.say(text)
        engine.runAndWait()
        speech_queue.task_done()

# Start TTS thread
tts_thread = threading.Thread(target=tts_worker, daemon=True)
tts_thread.start()

# Speech recognition
def listen_command(timeout=5, phrase_time_limit=7):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for voice command...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            return None
        except sr.RequestError:
            print("Error with the speech recognition service.")
            return None

# Gesture recognition
def detect_gesture(frame, results):
    global active, shutdown_flag, last_spoken
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_base = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
            index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            if thumb_tip.y < thumb_base.y and thumb_tip.y < index_tip.y:
                gesture_text = "Thumbs Up - Activating Dhruva"
                cv2.putText(frame, gesture_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                if not active and gesture_text != last_spoken:
                    speech_queue.put("Hello! I'm Dhruva, ready to assist you.")
                    last_spoken = gesture_text
                    active = True

            elif thumb_tip.y > thumb_base.y and thumb_tip.y > index_tip.y:
                gesture_text = "Thumbs Down - Shutting Down Dhruva"
                cv2.putText(frame, gesture_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                if active and gesture_text != last_spoken:
                    speech_queue.put("Goodbye! Take care and see you soon!")
                    last_spoken = gesture_text
                    shutdown_flag = True

# --- ABCD Poems Functionality ---
def speak_poem(text):
    print(f"Dhruva says: {text}")
    speech_queue.put(text)

poems = [
    """Twinkle, twinkle, little star,
How I wonder what you are!
Up above the world so high,
Like a diamond in the sky.""",
    """Baa, baa, black sheep,
Have you any wool?
Yes sir, yes sir,
Three bags full.""",
    """Humpty Dumpty sat on a wall,
Humpty Dumpty had a great fall.
All the king's horses and all the king's men,
Couldn't put Humpty together again.""",
    """Jack and Jill went up the hill,
To fetch a pail of water.
Jack fell down and broke his crown,
And Jill came tumbling after.""",
    """The wheels on the bus go round and round,
Round and round, round and round.
The wheels on the bus go round and round,
All through the town.""",
    """Row, row, row your boat,
Gently down the stream.
Merrily, merrily, merrily, merrily,
Life is but a dream.""",
    """Rain, rain, go away,
Come again another day.
Little Johnny wants to play,
Rain, rain, go away."""
]

alphabet_teach = """A for Apple, B for Ball, C for Cat, D for Dog, 
E for Elephant, F for Fish, G for Goat, H for Hat, 
I for Ice cream, J for Joker, K for Kite, L for Lion, M for Monkey, N for Nest, 
O for Orange, P for Parrot, Q for Queen, R for Rabbit, S for Sun, T for Tiger, 
U for Umbrella, V for Van, W for Watch, X for Xylophone, Y for Yak, Z for Zebra."""

# --- Math Algorithms Functionality ---
def extract_numbers(text):
    return [float(num) for num in re.findall(r"\d+(?:\.\d+)?", text)]

def parse_input(user_input):
    corrections = {
        'sine': r'sine|sign|sin',
        'cosine': r'cosine|cos|cosign',
        'tangent': r'tangent|tan',
        'log': r'logarithm|log base 10|log of|log',
        'ln': r'natural log|ln',
        'sqrt': r'square root|sqrt',
        'add': r'add|sum|\+|plus|summation of',
        'subtract': r'subtract|minus|\-|difference between',
        'multiply': r'multiply|product|\*|times|into',
        'divide': r'divided by|quotient|/',
        'power': r'power|raised to|to the power of|\*\*',
        'percent': r'percent of|% of|%',
        'factorial': r'factorial'
    }

    for key, pattern in corrections.items():
        if re.search(pattern, user_input):
            numbers = extract_numbers(user_input)
            return key, numbers

    return None, []

def perform_operation(op, nums):
    try:
        if op == 'add':
            return f"The result is {nums[0] + nums[1]}" if len(nums) >= 2 else "Provide two numbers."
        elif op == 'subtract':
            return f"The result is {nums[0] - nums[1]}" if len(nums) >= 2 else "Provide two numbers."
        elif op == 'multiply':
            return f"The result is {nums[0] * nums[1]}" if len(nums) >= 2 else "Provide two numbers."
        elif op == 'divide':
            return f"The result is {nums[0] / nums[1]}" if len(nums) >= 2 and nums[1] != 0 else "Cannot divide by zero."
        elif op == 'power':
            return f"{nums[0]} raised to {nums[1]} is {math.pow(nums[0], nums[1])}" if len(nums) >= 2 else "Provide two numbers."
        elif op == 'sqrt':
            return f"The square root is {math.sqrt(nums[0])}" if nums else "Provide a number."
        elif op == 'factorial':
            return f"The factorial is {math.factorial(int(nums[0]))}" if nums and nums[0].is_integer() and nums[0] >= 0 else "Provide a non-negative integer."
        elif op == 'log':
            return f"The log is {math.log10(nums[0])}" if nums else "Provide a number."
        elif op == 'ln':
            return f"The natural log is {math.log(nums[0])}" if nums else "Provide a number."
        elif op == 'sine':
            return f"The sine is {math.sin(math.radians(nums[0]))}" if nums else "Provide a number."
        elif op == 'cosine':
            return f"The cosine is {math.cos(math.radians(nums[0]))}" if nums else "Provide a number."
        elif op == 'tangent':
            return f"The tangent is {math.tan(math.radians(nums[0]))}" if nums else "Provide a number."
        else:
            return "Operation not supported."
    except Exception as e:
        return f"Error: {e}"

# --- Weather and Time Functionality ---
def get_weather(city):
    try:
        base_url = "https://api.openweathermap.org/data/2.5/weather"
        params = {"q": city, "appid": "6d31c19b9abf5128f624334bdbd92bdd", "units": "metric"}
        response = requests.get(base_url, params=params).json()

        if "weather" in response and "main" in response:
            desc = response["weather"][0]["description"]
            temp = response["main"]["temp"]
            return f"In {city}, it is {desc} with a temperature of {temp}°C."
        return "Couldn't fetch weather details."
    except Exception as e:
        return f"Error: {e}"

def get_current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%A, %d %B %Y"), now.strftime("%I:%M %p")

# --- Main Dhruva Functionality ---
def run_dhruva():
    global active, shutdown_flag
    cap = cv2.VideoCapture(0)
    while True:
        if shutdown_flag:
            break

        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb_frame)
        detect_gesture(frame, results)

        cv2.imshow("Dhruva Assistant", frame)

        if not active:
            command = listen_command()
            if command and ("dhruva" in command or "hello dhruva" in command):
                active = True
                speech_queue.put("Hello! I'm Dhruva, your friendly companion. How can I assist you today?")

        if active:
            command = listen_command()
            if not command:
                continue
            if "poem" in command:
                speak_poem(random.choice(poems))
            elif "alphabet" in command:
                speak_poem(alphabet_teach)
            elif "math" in command:
                op, nums = parse_input(command)
                result = perform_operation(op, nums)
                speech_queue.put(result)
            elif "weather" in command:
                speech_queue.put("Which city's weather would you like to know?")
                city = listen_command()
                if city:
                    speech_queue.put(get_weather(city))
            elif "time" in command:
                _, current_time = get_current_datetime()
                speech_queue.put(f"The current time is {current_time}.")
            elif "date" in command:
                current_date, _ = get_current_datetime()
                speech_queue.put(f"Today's date is {current_date}.")
            elif any(cmd in command for cmd in ["bye dhruva", "shutdown", "exit", "quit"]):
                shutdown_flag = True
                speech_queue.put("Goodbye! I hope you had a wonderful time. Take care!")
            else:
                speech_queue.put("I'm not sure how to help with that, but I'm learning new things every day!")

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    speech_queue.put("EXIT")
    tts_thread.join()

if __name__ == "__main__":
    run_dhruva()
    print("Dhruva Assistant has stopped.")