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

def get_current_datetime():
    now = datetime.datetime.now()
    return now.strftime("%A, %d %B %Y"), now.strftime("%I:%M %p")

def get_weather(city):
    API_KEY = '6d31c19b9abf5128f624334bdbd92bdd'
    url = f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric'
    try:
        response = requests.get(url).json()
        if 'weather' in response:
            desc = response['weather'][0]['description']
            temp = response['main']['temp']
            return f"In {city}, it's {desc} and {temp}°C."
        else:
            return "Couldn't find that city."
    except:
        return "Error retrieving weather."

gesture_queue = queue.Queue()

def gesture_detector():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
    mp_draw = mp.solutions.drawing_utils
    cap = cv2.VideoCapture(0)
    last_time = time.time()
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Count fingers for the left or right hand
                finger_tips = [8, 12, 16, 20]
                finger_states = []
                for tip in finger_tips:
                    if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip - 2].y:
                        finger_states.append(1)
                    else:
                        finger_states.append(0)
                fingers_up = sum(finger_states)
                cv2.putText(frame, f"Fingers: {fingers_up}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
                thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP]

                if time.time() - last_time > 2:
                    if thumb_tip.y < thumb_ip.y:
                        gesture_queue.put("approval")
                    elif thumb_tip.y > thumb_ip.y:
                        gesture_queue.put("disapproval")
                    last_time = time.time()
        cv2.imshow("Gesture Detection & Finger Counting", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def run_finger_and_face_detection():
    mp_hands = mp.solutions.hands
    mp_face = mp.solutions.face_mesh
    mp_drawing = mp.solutions.drawing_utils
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    face = mp_face.FaceMesh(max_num_faces=1)

    cap = cv2.VideoCapture(0)
    prev_count = -1

    def count_fingers(hand_landmarks, hand_label):
        tips_ids = [4, 8, 12, 16, 20]
        fingers = []
        if hand_label == "Right":
            fingers.append(1 if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x else 0)
        else:
            fingers.append(1 if hand_landmarks.landmark[tips_ids[0]].x > hand_landmarks.landmark[tips_ids[0] - 1].x else 0)
        for id in range(1, 5):
            fingers.append(1 if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id] - 2].y else 0)
        return sum(fingers)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        hand_results = hands.process(rgb)
        face_results = face.process(rgb)
        total_fingers = 0

        if hand_results.multi_hand_landmarks and hand_results.multi_handedness:
            for hand_landmarks, hand_handedness in zip(hand_results.multi_hand_landmarks, hand_results.multi_handedness):
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                total_fingers += count_fingers(hand_landmarks, hand_handedness.classification[0].label)

            if total_fingers != prev_count:
                speak(f"{total_fingers} fingers detected")
                prev_count = total_fingers

        if face_results.multi_face_landmarks:
            for face_landmarks in face_results.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    frame, face_landmarks,
                    mp_face.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1)
                )

        cv2.putText(frame, f'Fingers: {total_fingers}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Dhruva - Fingers and Face", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils
    hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
    cap = cv2.VideoCapture(0)
    prev_count = -1

    def count_fingers(hand_landmarks, hand_label):
        tips_ids = [4, 8, 12, 16, 20]
        fingers = []
        if hand_label == "Right":
            fingers.append(1 if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x else 0)
        else:
            fingers.append(1 if hand_landmarks.landmark[tips_ids[0]].x > hand_landmarks.landmark[tips_ids[0] - 1].x else 0)
        for id in range(1, 5):
            fingers.append(1 if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id] - 2].y else 0)
        return sum(fingers)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        total_fingers = 0

        if results.multi_hand_landmarks and results.multi_handedness:
            for hand_landmarks, hand_handedness in zip(results.multi_hand_landmarks, results.multi_handedness):
                mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                total_fingers += count_fingers(hand_landmarks, hand_handedness.classification[0].label)

            if total_fingers != prev_count:
                speak(f"{total_fingers} fingers detected")
                prev_count = total_fingers

        cv2.putText(frame, f'Fingers: {total_fingers}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.imshow("Dhruva Finger Counter", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
    cv2.destroyAllWindows()

def execute_command(command):
    if "poem" in command:
        speak(random.choice(poems))
    elif "alphabet" in command:
        speak(alphabet_teach)
    elif "weather" in command:
        speak("Which city?")
        city = listen_command()
        speak(get_weather(city))
    elif "time" in command:
        _, now = get_current_datetime()
        speak(f"It's {now}")
    elif "date" in command:
        today, _ = get_current_datetime()
        speak(f"Today is {today}")
    elif "fingers" in command or "face" in command:
        speak("Starting finger and face detection mode.")
        run_finger_and_face_detection()
        speak("Starting finger counting mode.")
        run_finger_and_face_detection()
        today, _ = get_current_datetime()
        speak(f"Today is {today}")
    else:
        op, nums = parse_input(command)
        if op:
            speak(perform_operation(op, nums))
        else:
            speak("I didn't understand that.")

def run_dhruva():
    threading.Thread(target=gesture_detector, daemon=True).start()
    speak("Dhruva is ready. Say 'Dhruva' or show thumbs up to begin.")
    active = False
    while True:
        if not gesture_queue.empty():
            gesture = gesture_queue.get()
            if gesture == "approval":
                speak("I'm listening!")
                active = True
            elif gesture == "disapproval":
                speak("Goodbye!")
                break
        command = listen_command()
        if command:
            if "dhruva" in command:
                speak("Yes, how can I help?")
                active = True
            elif any(word in command for word in ["stop", "exit", "shutdown"]):
                speak("Shutting down.")
                break
            elif active:
                execute_command(command)

if __name__ == "__main__":
    run_dhruva()
