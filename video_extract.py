import cv2
import os
from pathlib import Path

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


def extract_frames_dir(input_dir, interval=0.1, pattern="*.mp4", output_subdir="frames"):
    """Batch-extract frames for every video matched by `pattern` under `input_dir`.

    For each matched video, frames are written to `<video_parent>/<output_subdir>/`.
    Returns the list of output directories that were populated.
    """
    input_dir = Path(input_dir)
    outputs = []
    for video in sorted(input_dir.rglob(pattern)):
        out_dir = video.parent / output_subdir
        print(f"Extracting {video} -> {out_dir}")
        extract_frames(str(video), str(out_dir), interval=interval)
        outputs.append(out_dir)
    return outputs


# Usage
if __name__ == "__main__":
    # Original single-video call (kept for compatibility)
    # extract_frames("/home/haowei/Documents/TeraSim/CrashCase_HD_Video_rendered/crash_2023298086/final_bev.mp4",
    #                "/home/haowei/Documents/TeraSim/CrashCase_HD_Video_rendered/crash_2023298086/frames", 0.1)

    # Batch hdmap cameras (6 ftheta_camera_* subdirs, one .mp4 each)
    # extract_frames_dir(
    #     "/home/haowei/Documents/TeraSim-Agent/TeraSim/CrashCase_HD_Video_rendered/crash_2023174894/hdvideo/vehicle0_1_1_5_0/render/hdmap",
    #     interval=0.1,
    # )

    # Multiview composite video
    extract_frames(
        "/home/haowei/Documents/TeraSim-Agent/TeraSim/CrashCase_HD_Video_rendered/crash_2023174894/multiview/output_camera_10002_multi_view_10018.mp4",
        "/home/haowei/Documents/TeraSim-Agent/TeraSim/CrashCase_HD_Video_rendered/crash_2023174894/multiview/frames",
        0.1,
    )