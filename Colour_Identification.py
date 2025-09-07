import pandas as pd
import cv2
from scipy.spatial import KDTree

# Directory containing the RGB color palette chunk files
chunk_files = [
      "rgb_color_palette_with_names_chunk_1.csv",
    "rgb_color_palette_with_names_chunk_2.csv",
    "rgb_color_palette_with_names_chunk_3.csv",
    "rgb_color_palette_with_names_chunk_4.csv",
    "rgb_color_palette_with_names_chunk_5.csv",
    "rgb_color_palette_with_names_chunk_6.csv",
    "rgb_color_palette_with_names_chunk_7.csv",
    "rgb_color_palette_with_names_chunk_8.csv",
    "rgb_color_palette_with_names_chunk_9.csv",
    "rgb_color_palette_with_names_chunk_10.csv",
    "rgb_color_palette_with_names_chunk_11.csv",
    "rgb_color_palette_with_names_chunk_12.csv",
    "rgb_color_palette_with_names_chunk_13.csv",
    "rgb_color_palette_with_names_chunk_14.csv",
    "rgb_color_palette_with_names_chunk_15.csv",
    "rgb_color_palette_with_names_chunk_16.csv",
]

# Load all chunks and build a KDTree for efficient color matching
def load_color_data():
    all_colors = pd.DataFrame()
    for file in chunk_files:
        print(f"Loading {file}...")
        chunk = pd.read_csv(file)
        all_colors = pd.concat([all_colors, chunk], ignore_index=True)

    # Create a KDTree for fast color matching
    tree = KDTree(all_colors[['R', 'G', 'B']].values)
    return all_colors, tree

# Function to find the closest color
def get_closest_color(rgb, all_colors, tree):
    _, index = tree.query(rgb)
    return all_colors.iloc[index]['ColorName']

# Live feed color detection
def detect_color_live_feed():
    # Load color data and KDTree
    print("Loading color data...")
    all_colors, tree = load_color_data()
    print("Color data loaded.")

    # Initialize webcam
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Unable to access the camera.")
        return

    print("Starting color detection. Press 'q' to stop.")
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video frame.")
            break

        # Get the center pixel's RGB value
        height, width, _ = frame.shape
        center = (width // 2, height // 2)
        center_color_bgr = frame[center[1], center[0]]  # BGR format
        center_color_rgb = center_color_bgr[::-1]  # Convert to RGB

        # Get the closest color name
        detected_color = get_closest_color(center_color_rgb, all_colors, tree)

        # Display the detected color in the terminal
        print(f"Detected Color: {detected_color} (RGB: {tuple(center_color_rgb)})")

        # Show the live feed without visual indicators
        cv2.imshow("Live Color Detection", frame)

        # Break on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the color detection
detect_color_live_feed()
