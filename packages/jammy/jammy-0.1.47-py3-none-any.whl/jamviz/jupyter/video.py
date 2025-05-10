import base64
from io import BytesIO
from pathlib import Path
from typing import Optional, Union

from IPython.display import HTML, display


def display_video(  # pylint: disable=too-many-arguments
    file: Union[str, Path, bytes, bytearray, BytesIO],
    width: Optional[int] = 640,
    height: Optional[int] = 480,
    autoplay: bool = False,
    loop: bool = False,
    muted: bool = False,
) -> None:
    """
    Display a video file in a Jupyter Notebook using a data URL.

    Args:
        file (Union[str, Path, bytes, bytearray, BytesIO]): The video file to display.
            Can be a file path (str or Path) or video data (bytes, bytearray, or BytesIO).
        width (Optional[int]): The width of the video player in pixels. Set to None for default size.
        height (Optional[int]): The height of the video player in pixels. Set to None for default size.
        autoplay (bool): Whether the video should start playing automatically.
        loop (bool): Whether the video should loop when it reaches the end.
        muted (bool): Whether the video should be muted by default.

    Raises:
        FileNotFoundError: If the specified file path does not exist.
        ValueError: If the input type is not supported.
    """
    # Handle different input types
    if isinstance(file, (str, Path)):
        file_path = Path(file)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, "rb") as f:
            video = f.read()
    elif isinstance(file, (bytes, bytearray)):
        video = bytes(file)
    elif isinstance(file, BytesIO):
        video = file.getvalue()
    else:
        raise ValueError(f"Unsupported input type: {type(file)}")

    # Encode video data as base64
    video_url = f"data:video/mp4;base64,{base64.b64encode(video).decode('utf-8')}"

    # Prepare video attributes
    attributes = []
    if width is not None:
        attributes.append(f'width="{width}"')
    if height is not None:
        attributes.append(f'height="{height}"')
    if autoplay:
        attributes.append("autoplay")
    if loop:
        attributes.append("loop")
    if muted:
        attributes.append("muted")
    attributes.append("controls")

    # Create HTML for video player
    video_html = f"""
    <video {' '.join(attributes)}>
        <source src="{video_url}" type="video/mp4">
        Your browser does not support the video tag.
    </video>
    """
    display(HTML(video_html))
