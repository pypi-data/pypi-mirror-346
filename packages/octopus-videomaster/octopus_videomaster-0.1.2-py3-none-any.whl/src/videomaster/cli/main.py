"""命令行接口主模块"""

import os
import logging
import time
from pathlib import Path
from typing import Optional, List

import typer
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, TimeElapsedColumn
from rich.table import Table

from src.videomaster.core.processor import VideoProcessor
from src.videomaster.models.video_processor import VideoProcessingOptions, SubtitleArea
from src.videomaster.utils import helpers


# 加载环境变量
if "RUNNER_TEMP" in os.environ:
    from dotenv import load_dotenv
    load_dotenv()

app = typer.Typer(
    name="videomaster",
    help="VideoMaster: A powerful video processing tool.",
    add_completion=False
)

console = Console()
logger = logging.getLogger(__name__)

@app.command("process_video")
def process_video(
    input_path: Path = typer.Argument(..., help="Input video file path."),
    output: Optional[Path] = typer.Option(None, "--output", "-o", help="Output video file path."),
    rotate: Optional[float] = typer.Option(None, "--rotate", "-r", help="Rotate the video by this angle (in degrees)."),
    scale: Optional[float] = typer.Option(None, "--scale", "-sc", help="Scale the video by this factor."),
    speed: Optional[float] = typer.Option(None, "--speed", "-sp", help="Speed up or slow down the video by this factor."),
    flip_h: Optional[bool] = typer.Option(False, "--fliph", "-fh", help="Flip the video horizontally."),
    flip_v: Optional[bool] = typer.Option(False, "--flipv", "-fv", help="Flip the video vertically."),
    noise: Optional[int] = typer.Option(None, "--noise", "-n", help="Add noise to the video."),
    blur: Optional[int] = typer.Option(None, "--blur", "-b", help="Add blur to the video."),
    delete_frame: Optional[int] = typer.Option(None, "--delete-frame", "-df", help="Delete every n seconds a frame."),
    insert_frame: Optional[int] = typer.Option(None, "--insert-frame", "-if", help="Insert a frame every n seconds."),
    insert_image: Optional[Path] = typer.Option(None, "--insert-image", "-ii", help="Insert an image overlay."),
    log_level: str = typer.Option("INFO", "--log-level", help="Set the logging level.")
):
    """
    Process a video file with specified options.
    
    Args:
        input_path (Path): Path to the input video file.
        output (Optional[Path]): Path to save the processed video file.
        rotate (Optional[float]): Angle to rotate the video.
        scale (Optional[float]): Factor to scale the video.
        speed (Optional[float]): Factor to change the speed of the video.
        flip_h (Optional[bool]): Whether to flip the video horizontally.
        flip_v (Optional[bool]): Whether to flip the video vertically.
        noise (Optional[int]): Amount of noise to add to the video.
        delete_frame (Optional[int]): Delete every n frames a frame.
        insert_frame (Optional[int]): Insert a frame every n frames.
        insert_image (Optional[Path]): Path to the image to overlay on the video.
        log_level (str): Logging level. Default is INFO.
    """
    try:
        # 设置日志级别
        helpers.setup_logging(log_level)

        # 检查依赖项
        check_passed, error_message = helpers.check_dependencies()
        if not check_passed:
            console.print(f"\n[bold red]Error: {error_message}[/bold red]")
            raise typer.Exit(code=1)
        
        # 检查输入文件是否存在
        if not input_path.exists():
            console.print(f"\n[bold red]Error: Input file '{input_path}' does not exist.[/bold red]")
            raise typer.Exit(code=1)
        
        # 创建视频处理选项对象
        options = VideoProcessingOptions(
            input_path=input_path,
            output_path=output,
            rotate=rotate,
            scale=scale,
            speed=speed,
            flip_h=flip_h,
            flip_v=flip_v,
            noise=noise,
            blur=blur,
            delete_frame=delete_frame,
            insert_frame=insert_frame,
            insert_image=insert_image
        )

        # 打印处理信息
        console.print("\n[bold blue]VideoMaster - 视频处理[/bold blue]")
        console.print(f"Input file: [green]{input_path}[/green]")
        console.print(f"Output file: [green]{options.output_path}[/green]")
        console.print("\n[bold]Processing...[/bold]")

        # 显示处理进度
        start_time = time.time()

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            progress_task = progress.add_task("[bold blue]Processing", total=None)

            # 创建视频处理器实例
            processor = VideoProcessor()

            # 处理视频
            result = processor.process_video(options)

            if result.success:
                progress.update(progress_task, completed=1)
                elapsed_time = time.time() - start_time
                console.print(f"\n[bold green]Completed![/bold green] Time: {elapsed_time:.2f} seconds")
                
                table = Table(title="Processing Result")
                table.add_column("Output Type", justify="left", style="cyan")
                table.add_column("Output Path", justify="left", style="green")

                table.add_row("Video", str(result.output_path))
                console.print(table)
            else:
                console.print(f"\n[bold red]Error: {result.error_message}[/bold red]")
                raise typer.Exit(code=1)

    except Exception as e:
        logger.error(f"Error processing video: {str(e)}", exc_info=True)
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        raise typer.Exit(code=1)


@app.command('info')
def video_info(input_path: Path = typer.Argument(..., help="输入视频路径")):
    """
    获取视频信息
    
    Args:
        input_path (Path): 输入视频路径
    """
    try:
        # 检查输入文件是否存在
        if not input_path.exists():
            console.print(f"\n[bold red]Error: Input file '{input_path}' does not exist.[/bold red]")
            raise typer.Exit(code=1)

        console.print(f"\n[bold blue]VideoMaster Pro - 视频信息[/bold blue]")
        console.print(f"输入文件: [green]{input_path}[/green]")

        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            console=console
        ) as progress:
            progress_task = progress.add_task("[bold blue]获取视频信息...", total=None)
            
            # 获取视频信息
            info = helpers.get_video_info(input_path)
            
            # 完成任务
            progress.update(progress_task, completed=True)
        
        if info:
            table = Table(title="视频信息")
            table.add_column("属性", style="cyan")
            table.add_column("值", style="green")
            
            if "width" in info and "height" in info:
                table.add_row("分辨率", f"{info['width']}x{info['height']}")
            
            if "duration" in info:
                table.add_row("时长", f"{float(info['duration']):.2f}秒")
            
            if "bit_rate" in info:
                table.add_row("比特率", f"{int(info['bit_rate'])/1000:.2f} Kbps")
            
            if "avg_frame_rate" in info:
                # 解析帧率（通常是形如 "24000/1001" 的分数）
                frame_rate = info["avg_frame_rate"]
                if "/" in frame_rate:
                    num, den = map(int, frame_rate.split("/"))
                    if den != 0:
                        frame_rate = num / den
                    else:
                        frame_rate = 0
                table.add_row("帧率", f"{float(frame_rate):.2f} fps")
            
            console.print(table)
        else:
            console.print("[bold yellow]警告: 无法获取视频信息[/bold yellow]")

    except Exception as e:
        logger.error(f"Error getting video info: {str(e)}", exc_info=True)
        console.print(f"\n[bold red]Error: {str(e)}[/bold red]")
        raise typer.Exit(code=1)

@app.callback()
def main():
    """
    VideoMaster CLI - A powerful video processing tool.
    
    This tool allows you to process videos with various effects and options.
    """
    pass
if __name__ == "__main__":
    app()
