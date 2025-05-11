import argparse
import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, AudioFileClip
from moviepy.audio.fx import all as audio_fx

# === 模块功能 ===

def add_noise(frame, amount=10):
    noise = np.random.normal(0, amount, frame.shape).astype(np.int16)
    noisy = np.clip(frame.astype(np.int16) + noise, 0, 255)
    return noisy.astype(np.uint8)

def add_blur(frame, ksize=5):
    return cv2.GaussianBlur(frame, (ksize, ksize), 0)

def flip_horizontal(frame):
    return cv2.flip(frame, 1)

def flip_vertical(frame):
    return cv2.flip(frame, 0)

def resize_frame(frame, scale):
    height, width = frame.shape[:2]
    return cv2.resize(frame, (int(width * scale), int(height * scale)))

def insert_image_overlay(frame, image, alpha=0.5):
    image = cv2.resize(image, (frame.shape[1], frame.shape[0]))
    return cv2.addWeighted(frame, 1 - alpha, image, alpha, 0)

def delete_frame_condition(frame_index, fps, interval):
    return int(frame_index % (fps * interval)) == 0

# === 主处理逻辑 ===

def process_video(input_path, output_path, config):
    clip = VideoFileClip(input_path)
    fps = clip.fps
    frame_width, frame_height = clip.size
    total_frames = int(clip.duration * fps)

    overlay_img = None
    if config.insert_image:
        overlay_img = cv2.imread(config.insert_image, cv2.IMREAD_UNCHANGED)

    out = cv2.VideoWriter(
        "temp_video.mp4", cv2.VideoWriter_fourcc(*"mp4v"), fps, (frame_width, frame_height)
    )

    for i, frame in enumerate(clip.iter_frames()):
        if config.delete_interval and delete_frame_condition(i, fps, config.delete_interval):
            continue

        if config.flip_h:
            frame = flip_horizontal(frame)
        if config.flip_v:
            frame = flip_vertical(frame)
        if config.noise:
            frame = add_noise(frame)
        if config.blur:
            frame = add_blur(frame)
        if config.scale:
            frame = resize_frame(frame, config.scale)
            frame = cv2.resize(frame, (frame_width, frame_height))
        if config.border:
            frame = crop_and_border(frame, config.border)
        if overlay_img is not None and config.insert_interval:
            if i % int(fps * config.insert_interval) == 0:
                frame = insert_image_overlay(frame, overlay_img)

        out.write(frame[:, :, ::-1])  # Convert RGB to BGR

    out.release()

    # 替换音频
    if config.audio_speed:
        audio = clip.audio.fx(audio_fx.audio_speedx, config.audio_speed)
    else:
        audio = clip.audio

    final = VideoFileClip("temp_video.mp4")
    final = final.set_audio(audio)
    final.write_videofile(output_path, codec="libx264")

    os.remove("temp_video.mp4")

# === 命令行参数 ===

def parse_args():
    parser = argparse.ArgumentParser(description="视频反指纹处理工具")
    parser.add_argument("--input", required=True, help="输入视频路径")
    parser.add_argument("--output", required=True, help="输出视频路径")
    parser.add_argument("--noise", action="store_true", help="添加随机噪声")
    parser.add_argument("--blur", action="store_true", help="添加模糊")
    parser.add_argument("--flip_h", action="store_true", help="水平翻转")
    parser.add_argument("--flip_v", action="store_true", help="垂直翻转")
    parser.add_argument("--scale", type=float, help="缩放比例（如0.95）")
    parser.add_argument("--border", type=int, help="添加边框再裁剪")
    parser.add_argument("--delete_interval", type=int, help="每隔几秒删除一帧")
    parser.add_argument("--insert_image", type=str, help="插入图片路径")
    parser.add_argument("--insert_interval", type=int, help="每隔几秒插入一次图片")
    parser.add_argument("--audio_speed", type=float, help="音频变速，如1.05")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    process_video(args.input, args.output, args)
