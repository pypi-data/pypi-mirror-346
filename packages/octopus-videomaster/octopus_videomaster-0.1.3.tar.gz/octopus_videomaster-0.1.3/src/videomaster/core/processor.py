"""视频处理流程管理器"""

import logging
from pathlib import Path
from typing import Optional

from src.videomaster.core import video_effects_cv2
from src.videomaster.models.video_processor import ProcessingResult, VideoProcessingOptions

logger = logging.getLogger(__name__)


class VideoProcessor:
    """视频处理器，协调各个处理模块"""

    def process_video(self, options: VideoProcessingOptions) -> ProcessingResult:
        """处理视频

        Args:
            options: 视频处理选项

        Returns:
            处理结果
        """
        try:
            result = ProcessingResult(success=True)
            current_video_path = options.input_path
            
            # 应用特效
            needs_effects = (
                options.rotate is not None or
                options.scale is not None or
                options.speed is not None or
                options.delete_frame is not None or
                options.insert_frame is not None or
                options.insert_image is not None or
                options.flip_h is not None or
                options.flip_v is not None or
                options.noise is not None or
                options.blur is not None 
            )

            if needs_effects:
                logger.info("应用视频特效...")
                current_video_path = video_effects_cv2.apply_effects(options)
                result.output_path = current_video_path

            if result.output_path is None:
                if options.output_path:
                    # 如果没有进行任何处理但指定了输出路径，则直接复制输入文件
                    import shutil
                    shutil.copy(options.input_path, options.output_path)
                    result.output_path = options.output_path
                else:
                    # 如果没有进行任何处理且没有指定输出路径，则使用输入文件路径
                    result.output_path = options.input_path
                
            return result

        except Exception as e:
            logger.error(f"处理视频时发生错误: {str(e)}", exc_info=True)
            return ProcessingResult(success=False, error=str(e))
