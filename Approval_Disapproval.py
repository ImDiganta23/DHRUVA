import cv2
import mediapipe as mp
import pyttsx3
import threading
import queue
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

# Initialize text-to-speech
engine = pyttsx3.init()
speech_queue = queue.Queue()
last_spoken = ""

# Function to run the TTS engine from queue
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

# Webcam setup
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, landmarks, mp_hands.HAND_CONNECTIONS)

            thumb_tip = landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP]
            thumb_base = landmarks.landmark[mp_hands.HandLandmark.THUMB_CMC]
            index_tip = landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]

            if thumb_tip.y < thumb_base.y and thumb_tip.y < index_tip.y:
                gesture_text = "Thumb Up means Approval"
                cv2.putText(frame, gesture_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                if gesture_text != last_spoken:
                    speech_queue.put(gesture_text)
                    last_spoken = gesture_text

            elif thumb_tip.y > thumb_base.y and thumb_tip.y > index_tip.y:
                gesture_text = "Thumb Down means Disapproval"
                cv2.putText(frame, gesture_text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                if gesture_text != last_spoken:
                    speech_queue.put(gesture_text)
                    last_spoken = gesture_text

    cv2.imshow("Gesture Recognition", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Clean up
speech_queue.put("EXIT")
tts_thread.join()
cap.release()
cv2.destroyAllWindows()