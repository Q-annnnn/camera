import cv2
import os

# Create a directory to store the data if it doesn't exist
data_dir = "data"
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Get the last saved image number
image_files = [f for f in os.listdir(data_dir) if f.endswith(".jpg")]
if image_files:
    image_numbers = [int(f.split("_")[1].split(".")[0]) for f in image_files]
    image_number = max(image_numbers) + 1
else:
    image_number = 1

# Get the last saved video number
video_files = [f for f in os.listdir(data_dir) if f.endswith(".mp4")]
if video_files:
    video_numbers = [int(f.split("_")[1].split(".")[0]) for f in video_files]
    video_number = max(video_numbers)
else:
    video_number = 0

# Initialize the webcam
cap = cv2.VideoCapture(0)

# Set the image format
image_format = ".jpg"

# Define the codec and create a VideoWriter object for MP4 format (initialize as None)
out = None

recording = False  # Flag to indicate if we are recording

while True:
    # Capture a frame from the webcam
    ret, frame = cap.read()

    if recording:
        # If recording is active, write the frame to the output video
        if out is None:
            # Create the VideoWriter object when recording starts
            video_filename = os.path.join(data_dir, f"output_{video_number:04d}.mp4")
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(video_filename, fourcc, 20.0, (640, 480))
        out.write(frame)

    # Display the frame in the same window
    cv2.imshow('Webcam', frame)

    # Wait for a key press and check the key
    key = cv2.waitKey(1)

    if key == ord('q') or key == 27:  # 'q' or 'ESC' to exit
        break
    elif key == ord('s'):
        # Save the captured image to the data directory
        image_filename = os.path.join(data_dir, f"image_{image_number:04d}{image_format}")
        cv2.imwrite(image_filename, frame)
        print(f"Saved: {image_filename}")
        image_number += 1
    elif key == ord('r'):
        # Toggle recording on/off when 'r' is pressed
        if recording:
            print("Stopped recording")
            recording = False
            if out is not None:
                out.release()
                out = None
        else:
            print("Started recording")
            recording = True
            video_number += 1

# Release the webcam and the VideoWriter, and close the OpenCV windows
cap.release()
if out is not None:
    out.release()
cv2.destroyAllWindows()
