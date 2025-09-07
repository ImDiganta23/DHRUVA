import os
import cv2
import numpy as np
from tqdm import tqdm

# Define the corrected dataset path
DATASET_PATH = r"E:\Projects\Dhruva\asl_dataset"

# Set image properties
IMG_SIZE = 128  # Adjust based on your model input requirement
VALID_EXTENSIONS = {'.jpeg', '.jpg', '.png'}

# Storage for training data
X = []  # Images
y = []  # Labels

def validate_and_preprocess(dataset_path):
    if not os.path.exists(dataset_path):
        raise FileNotFoundError(f"Dataset path does not exist: {dataset_path}")

    print("Scanning dataset...")
    for label in sorted(os.listdir(dataset_path)):
        label_path = os.path.join(dataset_path, label)
        if not os.path.isdir(label_path) or not label.isalpha() or len(label) != 1:
            print(f"Skipping non-valid label folder: {label_path}")
            continue

        print(f"Processing label '{label}'...")
        for file in tqdm(os.listdir(label_path), desc=f"Loading {label}"):
            ext = os.path.splitext(file)[-1].lower()
            if ext not in VALID_EXTENSIONS:
                print(f"Skipping unsupported file: {file}")
                continue

            img_path = os.path.join(label_path, file)
            try:
                img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
                if img is None:
                    print(f"Could not load image: {img_path}")
                    continue
                img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
                img = img / 255.0  # Normalize to [0,1]
                X.append(img)
                y.append(ord(label.upper()) - ord('A'))  # Label as 0–25
            except Exception as e:
                print(f"Error processing {img_path}: {e}")

    print(f"\nLoaded {len(X)} images from dataset.")

    X_arr = np.array(X).reshape(-1, IMG_SIZE, IMG_SIZE, 1)
    y_arr = np.array(y)
    print(f"X shape: {X_arr.shape}, y shape: {y_arr.shape}")
    return X_arr, y_arr
