import cv2
import numpy as np

def process_video(input_path, output_path, logo_path):
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
    print(f"Video: {width}x{height}, FPS: {fps}")

    # Load and prepare logo
    logo = cv2.imread(logo_path, cv2.IMREAD_UNCHANGED)
    if logo is None:
        print("Error: Could not load logo.")
        return
        
    # Resize logo
    # Original is 1332x195. Let's make it width=800.
    target_w = 800
    target_h = int(logo.shape[0] * (target_w / logo.shape[1]))
    logo = cv2.resize(logo, (target_w, target_h), interpolation=cv2.INTER_AREA)
    
    # Split alpha
    if logo.shape[2] == 4:
        logo_bgr = logo[:, :, 0:3]
        logo_alpha = logo[:, :, 3] / 255.0
    else:
        logo_bgr = logo
        logo_alpha = np.ones((target_h, target_w))
        
    # The black box region
    # Previous crop was x=0, y=3400, w=900, h=440
    box_x1, box_y1 = 0, 3400
    box_x2, box_y2 = 1000, 3840  # slightly wider to assure covering
    
    # Center logo in this box
    box_w = box_x2 - box_x1
    box_h = box_y2 - box_y1
    
    logo_x = box_x1 + (box_w - target_w) // 2
    logo_y = box_y1 + (box_h - target_h) // 2
    
    # Set up the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

    print("Processing frames...")
    frame_count = 0
    
    while True:
        ret, frame = cap.read()
        if not ret:
            break
            
        # Draw black rectangle to hide the old logo
        cv2.rectangle(frame, (box_x1, box_y1), (box_x2, box_y2), (0, 0, 0), -1)
        
        # Overlay the new logo
        roi = frame[logo_y:logo_y+target_h, logo_x:logo_x+target_w]
        for c in range(0, 3):
            roi[:, :, c] = (logo_alpha * logo_bgr[:, :, c] + (1 - logo_alpha) * roi[:, :, c])
            
        frame[logo_y:logo_y+target_h, logo_x:logo_x+target_w] = roi

        out.write(frame)
        frame_count += 1
        
        if frame_count % 100 == 0:
            print(f"Processed {frame_count}/{total_frames}")

    cap.release()
    out.release()
    print("Done!")

if __name__ == "__main__":
    process_video("efe_promo_original.mp4", "efe_promo_new.mp4", "ss_logo_white.png")
