"""视频特效处理模块"""

import os
import logging
from pathlib import Path
from typing import Tuple

import cv2
import numpy as np
from moviepy import VideoFileClip, VideoClip, AudioClip, ImageSequenceClip, CompositeVideoClip

from src.videomaster.models.video_processor import VideoProcessingOptions
from src.videomaster.utils.decorators import runtime

logger = logging.getLogger(__name__)


def extract_video_audio(input_path: str) -> Tuple[VideoClip, AudioClip]:
    """提取视频音频

    Args:
        input_path: 输入视频文件路径
    Returns:
        Tuple[VideoClip, AudioClip]: 音频文件路径和视频文件路径
    """
    logger.info(f"提取音频和视频: {input_path}")
    clip = VideoFileClip(input_path)
    audio = clip.audio
    return clip, audio

def noise(frame, amount: int = 10):
    """在帧上添加噪声

    Args:
        frame: 输入帧
        amount: 噪声强度

    Returns:
        带噪声的帧
    """
    noise = np.random.normal(0, amount, frame.shape).astype(np.int16)
    noisy = np.clip(frame.astype(np.int16) + noise, 0, 255)
    return noisy.astype(np.uint8)

def blur(frame, ksize: int = 5):
    """在帧上添加模糊效果

    Args:
        frame: 输入帧
        ksize: 模糊核大小

    Returns:
        模糊后的帧
    """
    return cv2.GaussianBlur(frame, (ksize, ksize), 0)

def flip_horizontal(frame):
    """水平翻转帧"""
    return cv2.flip(frame, 1)

def flip_vertical(frame):
    """垂直翻转帧"""
    return cv2.flip(frame, 0)

def scale(frame, scale: float):
    """缩放帧
    Args:
        frame: 输入帧
        scale: 缩放比例
    Returns:
        缩放后的帧
    """
    height, width = frame.shape[:2]
    rsframe = cv2.resize(frame, (int(width * scale), int(height * scale)))
    return cv2.resize(rsframe, (width, height))

def insert_frame(frame, alpha=0.05):
    """在帧上插入图像覆盖层
    Args:
        frame: 输入帧
        image: 要插入的图像
        alpha: 透明度
    """
    # 获取项目根目录
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    # 构建图片文件的完整路径
    image_folder = os.path.join(project_root, 'assets')
    image_name = os.getenv('TRANSPARENT_PNG', 'blank_frame.png')
    image_path = os.path.join(image_folder, image_name)

    image = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    image = cv2.resize(image, (frame.shape[1], frame.shape[0]))
    if image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_BGRA2BGR)

    return cv2.addWeighted(frame, 1 - alpha, image, alpha, 0)

def delete_frame(frame_index, interval):
    """判断是否删除帧
    Args:
        frame_index: 当前帧索引
        interval: 帧数间隔
    Returns:
        bool: 是否删除当前帧
    """
    return int(frame_index % interval) == 0

def rotate(frame, angle: float):
    """旋转帧
    Args:
        frame: 输入帧
        angle: 旋转角度（度数）
    Returns:
        旋转后的帧
    """
    h, w = frame.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(frame, M, (w, h))

def audio_speed(audio: AudioClip, speed: float) -> AudioClip:
    """调整音频速度

    Args:
        audio: 输入音频剪辑
        speed: 速度倍率

    Returns:
        调整速度后的音频剪辑
    """
    logger.info(f"调整音频速度为 {speed}x")
    duration = audio.duration / speed
    fps = audio.fps

    def new_frame(t):
        """获取新音频帧"""
        # t = t * speed
        # if t > audio.duration:
        #     return None
        return audio.get_frame(t * speed)
    
    new_audio = AudioClip(new_frame, duration=duration, fps=fps)
    return new_audio


@runtime
def apply_effects(options: VideoProcessingOptions) -> Path:
    """应用视频特效

    Args:
        options: 视频处理选项

    Returns:
        处理后的视频路径
    """

    clip, audio = extract_video_audio(str(options.input_path))
    fps = clip.fps
    frame_width, frame_height = clip.size
    total_frames = int(clip.duration * fps)

    # 处理后的帧数组
    processed_frames = []

    # 写入输出文件
    output_path = options.output_path or Path(f"{options.input_path.stem}_processed{options.input_path.suffix}")
    
    final_fps = fps
    if options.speed:
        final_fps = fps * options.speed

    for i, frame in enumerate(clip.iter_frames()):
        # 删除帧
        if options.delete_frame is not None and options.delete_frame > 0 and delete_frame(i, options.delete_frame):
            continue

        # 微量旋转
        if options.rotate:
            frame = rotate(frame, options.rotate)
        # 水平镜像
        if options.flip_h:
            frame = flip_horizontal(frame)
        # 垂直镜像
        if options.flip_v:
            frame = flip_vertical(frame)
        # 添加噪声
        if options.noise:
            frame = noise(frame, options.noise)
        # 添加模糊
        if options.blur:
            frame = blur(frame, options.blur)
        # 缩放图像
        if options.scale:
            frame = scale(frame, options.scale)
        # 生成干扰帧
        if options.insert_frame is not None and options.insert_frame > 0:
            if i % int(options.insert_frame) == 0:
                frame = insert_frame(frame)

        processed_frames.append(frame)
    
    # out.release()
    # 创建处理后的视频剪辑
    processed_clip = ImageSequenceClip(processed_frames, fps=final_fps)

    # 如果视频有变速，则对音频进行相应的变速处理
    if options.speed:
        audio = audio_speed(audio, options.speed)
    
    # 合并音频和视频
    final_clip = CompositeVideoClip([processed_clip]).with_audio(audio)
    final_clip.write_videofile(output_path, audio_codec="aac", codec="libx264", fps=final_fps, preset="ultrafast", logger=None)

    logger.info(f"保存处理后的视频: {output_path}")
    
    # 关闭剪辑释放资源
    processed_clip.close()
    final_clip.close()
    clip.close()
    audio.close()
    
    return output_path 

