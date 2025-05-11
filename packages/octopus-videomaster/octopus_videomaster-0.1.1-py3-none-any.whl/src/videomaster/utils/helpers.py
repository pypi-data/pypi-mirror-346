"""工具函数模块"""

import logging
import os
import subprocess
from pathlib import Path
from typing import List, Optional, Tuple

logger = logging.getLogger(__name__)


def setup_logging(log_level: str = "INFO") -> None:
    """设置日志

    Args:
        log_level: 日志级别
    """
    numeric_level = getattr(logging, log_level.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError(f"无效的日志级别: {log_level}")
    
    logging.basicConfig(
        level=numeric_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )


def check_dependencies() -> Tuple[bool, Optional[str]]:
    """检查依赖项是否已安装

    Returns:
        (是否检查通过, 错误信息)
    """
    # 检查FFmpeg
    try:
        subprocess.run(
            ["ffmpeg", "-version"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=True
        )
    except (subprocess.SubprocessError, FileNotFoundError):
        return False, "未找到FFmpeg，请确保已安装并添加到PATH环境变量中"
    
    return True, None


def create_directory_if_not_exists(directory_path: Path) -> None:
    """如果目录不存在则创建

    Args:
        directory_path: 目录路径
    """
    if not directory_path.exists():
        logger.info(f"创建目录: {directory_path}")
        directory_path.mkdir(parents=True, exist_ok=True)


def parse_subtitle_area(area_str: str) -> Tuple[int, int, int, int]:
    """解析字幕区域字符串

    Args:
        area_str: 格式为 "x1,y1,x2,y2" 的字符串

    Returns:
        (x1, y1, x2, y2) 元组
    """
    try:
        x1, y1, x2, y2 = map(int, area_str.split(','))
        return x1, y1, x2, y2
    except (ValueError, AttributeError):
        raise ValueError("字幕区域格式无效，应为 'x1,y1,x2,y2'")


def get_video_info(video_path: Path) -> dict:
    """获取视频信息

    Args:
        video_path: 视频文件路径

    Returns:
        包含视频信息的字典
    """
    try:
        # 使用FFprobe获取视频信息
        result = subprocess.run(
            [
                "ffprobe",
                "-v", "error",
                "-select_streams", "v:0",
                "-show_entries", "stream=width,height,duration,bit_rate,avg_frame_rate",
                "-of", "json",
                str(video_path)
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        
        import json
        data = json.loads(result.stdout)
        return data.get("streams", [{}])[0]
    except Exception as e:
        logger.error(f"获取视频信息时发生错误: {str(e)}")
        return {} 