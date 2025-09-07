import speech_recognition as sr
import pyttsx3
import random
import threading
import cv2
import mediapipe as mp
import time
import queue
import math
import re
import datetime
import requests

# === TTS Initialization ===
engine = pyttsx3.init()
engine.setProperty('rate', 170)
voices = engine.getProperty('voices')
for voice in voices:
    if "male" in voice.name.lower() or "david" in voice.name.lower():
        engine.setProperty('voice', voice.id)
        break

def speak(text):
    witty_responses = [
        "Got it!", "On it!", "Here we go!", "Absolutely!",
        "Coming right up!", "You got it!", "Sure thing!", "Of course!"
    ]
    response = f"{random.choice(witty_responses)} {text}"
    print(f"Dhruva says: {text}")
    engine.say(response)
    engine.runAndWait()

def listen_command(timeout=5, phrase_time_limit=8):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎙 Listening...")
        try:
            audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except (sr.WaitTimeoutError, sr.UnknownValueError):
            print("Didn't catch that.")
            return None
        except sr.RequestError:
            print("Speech service error.")
            return None

# === Poems & Alphabets ===
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

# === Face Tracking ===
mp_face_detection = mp.solutions.face_detection
mp_drawing = mp.solutions.drawing_utils

def detect_faces():
    cap = cv2.VideoCapture(0)
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty frame.")
                continue
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = face_detection.process(image)
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            if results.detections:
                for detection in results.detections:
                    mp_drawing.draw_detection(image, detection)
            cv2.imshow('Face Detection', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break
    cap.release()
    cv2.destroyAllWindows()

# === Finger Counting ===
mp_hands = mp.solutions.hands

def count_fingers():
    cap = cv2.VideoCapture(0)
    with mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5
    ) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty frame.")
                continue

            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                    landmarks = hand_landmarks.landmark

                    finger_tips = [4, 8, 12, 16, 20]
                    thumb_tip = 4
                    thumb_ip = 2

                    fingers = []
                    for i in range(1, 5):  # Index to Pinky
                        if landmarks[finger_tips[i]].y < landmarks[finger_tips[i] - 2].y:
                            fingers.append(1)
                        else:
                            fingers.append(0)

                    # Check thumb
                    if landmarks[thumb_tip].x > landmarks[thumb_ip].x:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                    total_fingers = sum(fingers)
                    cv2.putText(image, f'Fingers: {total_fingers}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

            cv2.imshow('Finger Counting', image)
            if cv2.waitKey(5) & 0xFF == 27:
                break

    cap.release()
    cv2.destroyAllWindows()

# === Math Operations ===
def extract_numbers(text):
    return [float(num) for num in re.findall(r"\d+(?:\.\d+)?", text)]

def parse_input(user_input):
    corrections = {
        'sine': r'sine|sign|sin', 'cosine': r'cosine|cos|cosign', 'tangent': r'tangent|tan',
        'log': r'logarithm|log base 10|log of|log', 'ln': r'natural log|ln', 'sqrt': r'square root|sqrt',
        'add': r'add|sum|\+|plus|summation of', 'subtract': r'subtract|minus|\-|difference between',
        'multiply': r'multiply|product|\*|times|into', 'divide': r'divided by|quotient|/',
        'power': r'power|raised to|to the power of|\*\*', 'percent': r'percent of|% of|%', 'factorial': r'factorial'
    }
    for key, pattern in corrections.items():
        if re.search(pattern, user_input):
            numbers = extract_numbers(user_input)
            return key, numbers
    return None, []

def perform_operation(op, nums):
    try:
        if op == 'add': return f"The result is {nums[0] + nums[1]}"
        elif op == 'subtract': return f"The result is {nums[0] - nums[1]}"
        elif op == 'multiply': return f"The result is {nums[0] * nums[1]}"
        elif op == 'divide': return f"The result is {nums[0] / nums[1]}" if nums[1] != 0 else "Cannot divide by zero."
        elif op == 'power': return f"{nums[0]} raised to {nums[1]} is {math.pow(nums[0], nums[1])}"
        elif op == 'sqrt': return f"The square root of {nums[0]} is {math.sqrt(nums[0])}"
        elif op == 'percent': return f"{nums[0]}% of {nums[1]} is {(nums[0]/100) * nums[1]}"
        elif op == 'factorial': return f"The factorial of {int(nums[0])} is {math.factorial(int(nums[0]))}"
        elif op == 'log': return f"The log of {nums[0]} is {math.log10(nums[0])}"
        elif op == 'ln': return f"The natural log of {nums[0]} is {math.log(nums[0])}"
        elif op == 'sine': return f"The sine of {nums[0]} is {math.sin(math.radians(nums[0]))}"
        elif op == 'cosine': return f"The cosine of {nums[0]} is {math.cos(math.radians(nums[0]))}"
        elif op == 'tangent': return f"The tangent of {nums[0]} is {math.tan(math.radians(nums[0]))}"
    except:
        return "I couldn't compute that."

# === Main Execution ===
if __name__ == "__main__":
    speak("Hello! I'm Dhruva, your personal assistant. How can I help you today?")
    while True:
        command = listen_command()
        if command:
            if "poem" in command:
                speak(random.choice(poems))
            elif "alphabet" in command:
                speak(alphabet_teach)
            elif "face" in command and "track" in command:
                speak("Starting face tracking. Press ESC to exit.")
                detect_faces()
            elif "finger count" in command:
                speak("Starting finger counting. Press ESC to exit.")
                count_fingers()
            else:
                operation, numbers = parse_input(command)
                if operation and numbers:
                    speak(perform_operation(operation, numbers))
                else:
                    speak("I couldn't understand that. Could you repeat?")
