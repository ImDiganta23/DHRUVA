import pandas as pd

# Set the chunk size
chunk_size = 1048576
total_colors = 256**3  # Total combinations in the RGB color space
file_base_path = "rgb_color_palette_chunk"

# Function to generate chunks and save them
def generate_rgb_palette_in_chunks():
    chunk_data = []
    chunk_count = 0

    # Loop through all possible RGB combinations
    for r in range(256):
        for g in range(256):
            for b in range(256):
                chunk_data.append({"ColorName": f"{r}-{g}-{b}", "R": r, "G": g, "B": b})

                # When chunk size is reached, save to CSV
                if len(chunk_data) == chunk_size:
                    save_chunk(chunk_data, chunk_count)
                    chunk_data = []  # Reset the chunk data
                    chunk_count += 1

    # Save any remaining data
    if chunk_data:
        save_chunk(chunk_data, chunk_count)

    print(f"RGB color palette saved in {chunk_count + 1} chunks.")

# Function to save a single chunk to CSV
def save_chunk(data, chunk_number):
    df = pd.DataFrame(data)
    file_path = f"{file_base_path}_{chunk_number + 1}.csv"
    df.to_csv(file_path, index=False)
    print(f"Chunk {chunk_number + 1} saved as {file_path}")

# Run the function
generate_rgb_palette_in_chunks()
