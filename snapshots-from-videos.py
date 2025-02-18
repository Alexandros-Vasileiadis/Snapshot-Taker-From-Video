import os
import cv2
import shutil

def take_snapshots(video_file, frame_interval, output_base, delete_existing=False):
    # Create the full video path from the 'videos' folder
    video_path = os.path.join(os.getcwd(), "videos", video_file)
    if not os.path.exists(video_path):
        print(f"Error: Video file '{video_path}' not found.")
        return

    # create a snapshots subfolder
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    output_dir = os.path.join(output_base, f"{video_name}_snapshots")

    # delete existing snapshots folder if user requested it
    if os.path.exists(output_dir) and delete_existing:
        shutil.rmtree(output_dir)
        print(f"Deleted existing snapshots folder: {output_dir}")

    os.makedirs(output_dir, exist_ok=True)

    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"Cannot open video file '{video_path}'.")
        return

    frame_count = 0
    snapshot_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_count % frame_interval == 0:
            snapshot_name = f"snapshot_{snapshot_count:04d}_frame_{frame_count:04d}.jpg"
            snapshot_path = os.path.join(output_dir, snapshot_name)
            cv2.imwrite(snapshot_path, frame)
            snapshot_count += 1

        frame_count += 1

    cap.release()
    print(f"Finished processing '{video_file}'. Snapshots saved in '{output_dir}'.")

if __name__ == "__main__":
    # ask for frame interval
    frame_interval_input = input("Enter frame interval (frames between snapshots): ")
    try:
        frame_interval = int(frame_interval_input)
    except ValueError:
        print("Invalid input for frame interval. Using default value of 10.")
        frame_interval = 10

    # ask to delete previous snapshots if they exist
    delete_input = input("Delete previous snapshots if they exist? (y/n): ").strip().lower()
    delete_previous = delete_input.startswith("y")

    # directories
    current_dir = os.getcwd()
    video_dir = os.path.join(current_dir, "videos")
    snapshots_dir = os.path.join(current_dir, "snapshots")
    os.makedirs(snapshots_dir, exist_ok=True)

    # check if 'videos' folder exists
    if not os.path.exists(video_dir):
        print(f"Error: Videos folder '{video_dir}' not found.")
    else:
        for file in os.listdir(video_dir):
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
                print(f"Processing video: {file}")
                take_snapshots(file, frame_interval, snapshots_dir, delete_existing=delete_previous)
