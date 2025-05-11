"""视频特效处理模块"""

import logging
from pathlib import Path
from typing import Optional, Tuple

import cv2
import numpy as np
from moviepy import VideoFileClip, vfx

from src.videomaster.models.video_processor import VideoProcessingOptions
from src.videomaster.utils.decorators import runtime

logger = logging.getLogger(__name__)


@runtime
def rotate_video(clip, angle: float):
    """旋转视频

    Args:
        clip: MoviePy视频剪辑对象
        angle: 旋转角度（度数）

    Returns:
        旋转后的视频剪辑
    """
    logger.info(f"旋转视频 {angle} 度")
    return clip.with_effects([vfx.Rotate(angle=angle)])

@runtime
def scale_video(clip, scale: float):
    """缩放视频

    Args:
        clip: MoviePy视频剪辑对象
        scale: 缩放比例

    Returns:
        缩放后的视频剪辑
    """
    logger.info(f"缩放视频，比例: {scale}")
    new_width = int(clip.w * scale)
    new_height = int(clip.h * scale)
    return clip.with_effects([vfx.Resize(width=new_width, height=new_height)])

@runtime
def change_speed(clip, speed: float):
    """调整视频速度

    Args:
        clip: MoviePy视频剪辑对象
        speed: 速度倍率

    Returns:
        调整速度后的视频剪辑
    """
    logger.info(f"调整视频速度为 {speed}x")
    return clip.with_effects([vfx.MultiplySpeed(speed)])

@runtime
def mirror_x(clip):
    """水平翻转视频

    Args:
        clip: MoviePy视频剪辑对象

    Returns:
        水平翻转后的视频剪辑
    """
    logger.info("水平翻转视频")
    return clip.with_effects([vfx.MirrorX()])

@runtime
def mirror_y(clip):
    """垂直翻转视频

    Args:
        clip: MoviePy视频剪辑对象

    Returns:
        垂直翻转后的视频剪辑
    """
    logger.info("垂直翻转视频")
    return clip.with_effects([vfx.MirrorY()])


@runtime
def apply_effects(options: VideoProcessingOptions) -> Path:
    """应用视频特效

    Args:
        options: 视频处理选项

    Returns:
        处理后的视频路径
    """
    logger.info(f"加载视频: {options.input_path}")
    clip = VideoFileClip(str(options.input_path))
    
    # 应用效果
    if options.rotate is not None:
        clip = rotate_video(clip, options.rotate)
    
    if options.scale is not None:
        clip = scale_video(clip, options.scale)
    
    if options.speed is not None:
        clip = change_speed(clip, options.speed)
    
    # 写入输出文件
    output_path = options.output_path or Path(f"{options.input_path.stem}_processed{options.input_path.suffix}")
    logger.info(f"保存处理后的视频: {output_path}")
    clip.write_videofile(str(output_path))
    
    # 关闭剪辑释放资源
    clip.close()
    
    return output_path 
