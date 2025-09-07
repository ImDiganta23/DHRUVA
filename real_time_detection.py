import cv2
import pyttsx3
import torch
from torchvision import models, transforms
import wikipedia

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()

# Load Pre-trained Object Detection Model
model = models.detection.fasterrcnn_resnet50_fpn(pretrained=True)
model.eval()

# Image Transformation
transform = transforms.Compose([transforms.ToTensor()])

# Initialize camera
cap = cv2.VideoCapture(0)  # 0 for default webcam

if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

# Speak Text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Object Detection
def detect_object(image):
    tensor_image = transform(image).unsqueeze(0)
    predictions = model(tensor_image)[0]
    if len(predictions['scores']) > 0 and predictions['scores'][0] > 0.8:
        label = predictions['labels'][0].item()
        return label  # Return label
    return "unknown object"

# Get Additional Information
def fetch_object_info(object_name):
    try:
        summary = wikipedia.summary(object_name, sentences=2)
        return summary
    except Exception:
        return "I couldn't find more information about this object."

# Process Frame in Real-time
while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    if not ret:
        print("Failed to capture image")
        break

    # Convert frame to PIL image for object detection
    image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    label = detect_object(image)
    
    if label != "unknown object":
        response = f"I see a {label}."
        additional_info = fetch_object_info(label)
        response += f" {additional_info}"
        speak(response)

    # Show live video feed with detection result
    cv2.putText(frame, f"Detected: {label}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow("Real-time Object Detection", frame)

    # Exit loop when 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close windows
cap.release()
cv2.destroyAllWindows()
