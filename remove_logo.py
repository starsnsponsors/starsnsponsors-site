import cv2
import numpy as np

def process_video(input_path, output_path):
    print(f"Opening video: {input_path}")
    cap = cv2.VideoCapture(input_path)
    
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    # Get video properties
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    print(f"Properties - Resolution: {width}x{height}, FPS: {fps}, Total Frames: {total_frames}")

    # Set up the video writer
    # Using mp4v codec for MP4 files
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    # The region to blur/crop
    # Base on analysis: x=0, y=3400, w=900, h=440
    crop_x, crop_y = 0, 3400
    crop_w, crop_h = 900, 440

    print("Processing frames...")
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # We will apply a blur to the logo area
        # Extract the region of interest
        roi = frame[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w]
        
        # Apply a strong Gaussian blur to obfuscate the logo
        # The kernel size must be odd and positive
        blurred_roi = cv2.GaussianBlur(roi, (151, 151), 0)
        
        # Replace the ROI with the blurred version
        frame[crop_y:crop_y+crop_h, crop_x:crop_x+crop_w] = blurred_roi
        
        # Write the processed frame
        out.write(frame)
        
        frame_count += 1
        if frame_count % 100 == 0:
            print(f"Processed {frame_count}/{total_frames} frames ({(frame_count/total_frames)*100:.1f}%)")

    # Release everything
    cap.release()
    out.release()
    print(f"Finished processing! Saved to: {output_path}")

if __name__ == "__main__":
    input_file = "efe_promo.mp4"
    output_file = "efe_promo_nologo.mp4"
    process_video(input_file, output_file)
