"""视频处理模型定义"""

from pathlib import Path
from typing import List, Optional, Tuple, Union

from pydantic import BaseModel, Field, field_validator, FieldValidationInfo

class SubtitleArea(BaseModel):
    """字幕区域定义"""
    x1: int = Field(..., description="左上角x坐标")
    y1: int = Field(..., description="左上角y坐标")
    x2: int = Field(..., description="右下角x坐标")
    y2: int = Field(..., description="右下角y坐标")

    @field_validator('x2')
    def x2_must_be_greater_than_x1(cls, v, values):
        if 'x1' in values and v <= values['x1']:
            raise ValueError('x2 must be greater than x1')
        return v
    
    @field_validator('y2')
    def y2_must_be_greater_than_y1(cls, v, values):
        if 'y1' in values and v <= values['y1']:
            raise ValueError('y2 must be greater than y1')
        return v
    

class VideoProcessingOptions(BaseModel):
    """视频处理选项"""
    input_path: Path = Field(..., description="输入视频文件路径")
    output_path: Optional[Path] = None
    
    # 视频效果选项
    rotate: Optional[float] = Field(None, description="视频旋转角度")
    scale: Optional[float] = Field(None, description="视频缩放比例")
    speed: Optional[float] = Field(None, description="视频播放速度")
    flip_h: bool = Field(False, description="是否水平翻转")
    flip_v: bool = Field(False, description="是否垂直翻转")
    noise: Optional[int] = Field(None, description="添加噪声强度")
    blur: Optional[int] = Field(None, description="添加模糊强度")
    delete_frame: Optional[int] = Field(None, description="每隔n秒删除一帧")
    insert_frame: Optional[int] = Field(None, description="每隔n秒插入一帧")
    insert_image: Optional[Path] = Field(None, description="插入图片路径")

    # 字幕处理选项
    erase_subtitle: bool = Field(False, description="是否擦除字幕")
    subtitle_area: Optional[SubtitleArea] = Field(None, description="字幕区域")
    generate_acc: bool = Field(False, description="是否生成字幕")
    translate: Optional[str] = Field(None, description="翻译语言")

    # 音频处理选项
    add_audio: Optional[Path] = Field(None, description="添加音频文件路径")

    @field_validator('output_path')
    def set_default_output_path(cls, v, info):
        values = info.data
        if v is None and 'input_path' in values:
            input_path = values.get('input_path')
            stem = input_path.stem
            return Path(f"{stem}_processed{input_path.suffix}")
        return v

    @field_validator('rotate')
    def validate_rotation(cls, v):
        if v is not None and (v < 0 or v >= 360):
            raise ValueError('旋转角度必须在0-360度之间')
        return v

    @field_validator('scale')
    def validate_scale(cls, v):
        if v is not None and v <= 0:
            raise ValueError('缩放比例必须大于0')
        return v

    @field_validator('speed')
    def validate_speed(cls, v):
        if v is not None and v <= 0:
            raise ValueError('播放速度必须大于0')
        return v
    
    @field_validator('delete_frame', 'insert_frame')
    def validate_frame_interval(cls, v):
        if v is not None and v <= 0:
            raise ValueError('帧间隔必须大于0')
        return v
    
    @field_validator('insert_image')
    def validate_insert_image(cls, v):
        if v is not None and not v.exists():
            raise ValueError('插入图片路径不存在')
        return v

    @field_validator('subtitle_area')
    def validate_subtitle_area(cls, v, info):
        values = info.data
        if values.get('erase_subtitle', False) and v is None:
            raise ValueError('启用字幕擦除时必须指定字幕区域')
        return v
    

class ProcessingResult(BaseModel):
    """处理结果"""
    success: bool
    output_path: Optional[Path] = None
    subtitle_path: Optional[Path] = None
    translation_path: Optional[Path] = None
    error_message: Optional[str] = None 
    
