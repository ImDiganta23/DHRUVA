import cv2
import mediapipe as mp

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

# Initialize hands
hands = mp_hands.Hands(max_num_hands=8,
                       min_detection_confidence=0.7,
                       min_tracking_confidence=0.7)

# Tip landmarks
finger_tips = [4, 8, 12, 16, 20]  # Thumb to pinky
finger_mcp = [2, 6, 10, 14, 18]   # Corresponding lower joints

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)
    total_fingers = 0

    if results.multi_hand_landmarks and results.multi_handedness:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            handedness = results.multi_handedness[idx].classification[0].label
            lm = hand_landmarks.landmark

            fingers = []

            # Thumb logic: horizontal check (left vs right hand)
            if handedness == "Right":
                fingers.append(lm[finger_tips[0]].x < lm[finger_mcp[0]].x)
            else:
                fingers.append(lm[finger_tips[0]].x > lm[finger_mcp[0]].x)

            # Other fingers: vertical check
            for tip, pip in zip(finger_tips[1:], finger_mcp[1:]):
                fingers.append(lm[tip].y < lm[pip].y)

            total_fingers += sum(fingers)

            # Draw landmarks
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display total fingers
    cv2.putText(frame, f'Total Fingers: {total_fingers}', (10, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)

    cv2.imshow("10 Finger Counter", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()