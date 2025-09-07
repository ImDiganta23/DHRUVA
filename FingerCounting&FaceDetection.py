import cv2
import mediapipe as mp
import pyttsx3
import threading
import queue
import time

# Initialize TTS engine
engine = pyttsx3.init()
engine.setProperty('rate', 150)

# MediaPipe modules
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(min_detection_confidence=0.7, min_tracking_confidence=0.5)
face = mp_face.FaceMesh(max_num_faces=1)

# Queue for safe speech
speech_queue = queue.Queue()

# Count fingers function
def count_fingers(hand_landmarks, hand_label):
    tips_ids = [4, 8, 12, 16, 20]
    fingers = []

    # Thumb
    if hand_label == "Right":
        fingers.append(1 if hand_landmarks.landmark[tips_ids[0]].x < hand_landmarks.landmark[tips_ids[0] - 1].x else 0)
    else:
        fingers.append(1 if hand_landmarks.landmark[tips_ids[0]].x > hand_landmarks.landmark[tips_ids[0] - 1].x else 0)

    # Other fingers
    for id in range(1, 5):
        fingers.append(1 if hand_landmarks.landmark[tips_ids[id]].y < hand_landmarks.landmark[tips_ids[id] - 2].y else 0)

    return sum(fingers)

# Speak asynchronously
def speak_fingers():
    last_spoken_time = 0
    debounce_delay = 1.5  # seconds between allowed speeches
    while True:
        count = speech_queue.get()
        if count is None:
            break
        current_time = time.time()
        if current_time - last_spoken_time > debounce_delay:
            engine.say(f"{count} fingers")
            engine.runAndWait()
            last_spoken_time = current_time

# Start the speech thread
speech_thread = threading.Thread(target=speak_fingers, daemon=True)
speech_thread.start()

# Start webcam
cap = cv2.VideoCapture(0)
previous_count = -1

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    hand_results = hands.process(rgb)
    face_results = face.process(rgb)

    total_fingers = 0
    hands_detected = False

    if hand_results.multi_hand_landmarks and hand_results.multi_handedness:
        hands_detected = True
        for hand_landmarks, hand_handedness in zip(hand_results.multi_hand_landmarks, hand_results.multi_handedness):
            hand_label = hand_handedness.classification[0].label
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            total_fingers += count_fingers(hand_landmarks, hand_label)

    # Speak only if hands are visible and finger count changes
    if hands_detected and total_fingers != previous_count:
        speech_queue.put(total_fingers)
        previous_count = total_fingers

    # Face mesh drawing
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            mp_drawing.draw_landmarks(
                frame, face_landmarks,
                mp_face.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing.DrawingSpec(color=(0, 255, 255), thickness=1, circle_radius=1)
            )

    # Display fingers on screen
    cv2.putText(frame, f'Fingers: {total_fingers}', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

    cv2.imshow("Gesture & Face Detection", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC to exit
        break

cap.release()
cv2.destroyAllWindows()

# Gracefully stop the speech thread
speech_queue.put(None)
speech_thread.join()
