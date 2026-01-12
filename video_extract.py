import cv2
import os

def extract_frames(video_path, output_dir, interval=0.1):
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_interval = max(1, int(fps * interval))
    
    os.makedirs(output_dir, exist_ok=True)
    
    frame_count = 0
    saved_count = 0
    
    while cap.read()[0]:
        if frame_count % frame_interval == 0:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_count)
            ret, frame = cap.read()
            output_path = os.path.join(output_dir, f"frame_{saved_count:06d}.png")
            cv2.imwrite(output_path, frame)
            saved_count += 1
        frame_count += 1
    
    cap.release()

# Usage
extract_frames("/home/haowei/Documents/TeraSim/CrashCase_HD_Video_rendered/crash_2023298086/final_bev.mp4", 
                "/home/haowei/Documents/TeraSim/CrashCase_HD_Video_rendered/crash_2023298086/frames", 0.1)