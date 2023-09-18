import cv2
import os

def rotate_image(image_path, degrees):
    # Load the image
    img = cv2.imread(image_path)

    if img is not None:
        # Get the image dimensions
        height, width = img.shape[:2]

        # Calculate the rotation matrix
        rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), degrees, 1)

        # Apply the rotation to the image
        rotated_image = cv2.warpAffine(img, rotation_matrix, (width, height))

        # Save the rotated image
        cv2.imwrite(image_path, rotated_image)
        print(f"Rotated {image_path} by {degrees} degrees.")
    else:
        print(f"Could not load image: {image_path}")

def rotate_video(video_path, degrees):
    # Check if the video file exists
    if not os.path.exists(video_path):
        print(f"Video file not found: {video_path}")
        return

    # Open the video file
    cap = cv2.VideoCapture(video_path)

    if not cap.isOpened():
        print(f"Could not open video: {video_path}")
        return

    # Get the video frame dimensions
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Define the codec (mp4v) and create a VideoWriter object for the rotated video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    output_filename = os.path.splitext(os.path.basename(video_path))[0] + f"_rotate_{degrees}.mp4"
    output_path = os.path.join("data", output_filename)
    output_video = cv2.VideoWriter(output_path, fourcc, 20.0, (width, height))

    while True:
        ret, frame = cap.read()

        if not ret:
            break

        # Rotate the frame
        rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE * (degrees // 90))

        # Write the rotated frame to the output video
        output_video.write(rotated_frame)

    # Release the video objects
    cap.release()
    output_video.release()
    print(f"Rotated {video_path} by {degrees} degrees. Saved as {output_path}.")

# Input directory containing images and videos
data_dir = "data"

while True:
    choice = input("Enter 'i' to rotate an image, 'v' to rotate a video, or 'q' to quit: ").strip().lower()
    
    if choice == 'q':
        break
    
    numeric_identifier = input("Enter the numeric identifier (e.g., 0001): ")
    degrees = int(input("Enter rotation degrees: "))
    
    if choice == 'i':
        image_files = [f for f in os.listdir(data_dir) if f.startswith(f"image_{numeric_identifier}")]
        if image_files:
            for image_file in image_files:
                image_path = os.path.join(data_dir, image_file)
                rotate_image(image_path, degrees)
        else:
            print(f"No image files found with identifier {numeric_identifier}.")
    elif choice == 'v':
        video_files = [f for f in os.listdir(data_dir) if f.startswith(f"output_{numeric_identifier}")]
        if video_files:
            for video_file in video_files:
                video_path = os.path.join(data_dir, video_file)
                rotate_video(video_path, degrees)
        else:
            print(f"No video files found with identifier {numeric_identifier}.")

print("Rotation complete.")
