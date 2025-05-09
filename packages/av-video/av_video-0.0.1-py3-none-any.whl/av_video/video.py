import pathlib
import shutil
import tempfile
from typing import Any, Tuple

import av
from PIL import Image
from tqdm.auto import tqdm

# https://github.com/microsoft/vscode-docs/blob/main/release-notes/v1_72.md#built-in-preview-for-some-audio-and-video-files
_VIDEO_CODEC_SUPPORTED_BY_VSCODE = {
    "h264": "libx264",  # H.264
}

_IMAGE_FILE_SUFFIXES = [
    ".png",
    ".jpg",
    ".jpeg",
]


def _force_vscode_compatible(
    video: str | pathlib.Path,
    previewable_video: str | pathlib.Path | None = None,
) -> None:
    """Force a video file to a format supported by VSCode built-in preview."""
    video = pathlib.Path(video)

    if not video.exists():
        raise ValueError(f"Video file '{video}' does not exist")
    if not video.is_file():
        raise ValueError(f"'{video}' is not a file")

    with av.open(video) as container:
        stream = container.streams.video[0]

        # check if the video is already compatible with VSCode built-in preview
        if stream.codec.name in _VIDEO_CODEC_SUPPORTED_BY_VSCODE:
            return

        if previewable_video is None:
            previewable_video = video.parent / f"{video.stem}_previewable.mp4"

        if previewable_video.suffix != ".mp4":
            raise ValueError(
                f"Previewable video file must have '.mp4' suffix, got '{previewable_video.suffix}'"
            )
        if previewable_video.exists():
            raise RuntimeError(
                f"Previewable video file '{previewable_video}' already exists"
            )

        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as f:
            temp_file = f.name

        with av.open(temp_file, mode="w") as temp_container:
            temp_stream = temp_container.add_stream(
                _VIDEO_CODEC_SUPPORTED_BY_VSCODE["h264"],
                rate=stream.average_rate,
            )
            temp_stream.pix_fmt = "yuv420p"  # widely supported format for H.264

            frames = list(container.decode(stream))

            if len(frames) != stream.frames:
                raise RuntimeError(
                    f"Frames not matched in the video file '{video}'"
                )

            for frame in tqdm(
                frames,
                total=len(frames),
                desc="Forcing video to VSCode compatible format",
                unit="frame",
            ):
                packet = temp_stream.encode(frame)
                if packet:
                    temp_container.mux(packet)

            for packet in temp_stream.encode():
                temp_container.mux(packet)

        shutil.move(temp_file, previewable_video)


class VideoReader:
    """Object to read video files."""

    def __init__(self, file: str | pathlib.Path) -> None:
        """Open a video file for reading."""
        self._file: pathlib.Path = pathlib.Path(file)

        if not self._file.exists():
            raise ValueError(f"Video file '{self._file}' does not exist")
        if not self._file.is_file():
            raise ValueError(f"'{self._file}' is not a file")

        self.container: av.container.input.InputContainer = av.open(file)
        self.stream: av.video.VideoStream = self.container.streams.video[0]

    def close(self) -> None:
        """Close the video file."""
        if self.container and self.stream:
            self.container.close()
        self.container, self.stream = None, None

    def __enter__(self) -> "VideoReader":
        """Enter the context manager."""
        if self.container is None or self.stream is None:
            raise RuntimeError(f"Video file '{self._file}' is not opened")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager."""
        self.close()

    @property
    def is_vscode_compatible(self) -> bool:
        """Whether the video file is supported by VSCode built-in preview."""
        return self.stream.codec.name in _VIDEO_CODEC_SUPPORTED_BY_VSCODE

    def force_vscode_compatible(self) -> None:
        """Force the video file to a format supported by VSCode built-in preview."""
        _force_vscode_compatible(self._file)

    def to_images(
        self,
        dir: str | pathlib.Path | None = None,
        pattern: str = "color_{frame_id:05d}.png",
    ) -> None:
        """Convert the video file to a sequence of image files."""
        dir = (
            self._file.parent / self._file.stem
            if dir is None
            else pathlib.Path(dir)
        )

        dir.mkdir(parents=True, exist_ok=True)

        frames = list(self.container.decode(self.stream))

        if len(frames) != self.stream.frames:
            raise RuntimeError(
                f"Frames not matched in the video file '{self._file}'"
            )

        frame_id = 0

        for frame in tqdm(
            frames,
            total=len(frames),
            desc="Converting video to images",
            unit="frame",
        ):
            image = frame.to_image()
            file = dir / pattern.format(frame_id=frame_id)
            image.save(file)
            frame_id += 1


class VideoWriter:
    """Object to write video files."""

    def __init__(
        self, file: str | pathlib.Path, fps: int, size: Tuple[int, int]
    ) -> None:
        """Open a video file for writing."""
        self._file: pathlib.Path = pathlib.Path(file)

        self._file.parent.mkdir(parents=True, exist_ok=True)

        self.container: av.container.output.OutputContainer = av.open(
            file, mode="w"
        )
        self.stream: av.video.VideoStream = self.container.add_stream(
            _VIDEO_CODEC_SUPPORTED_BY_VSCODE["h264"], rate=fps
        )
        self.stream.pix_fmt = "yuv420p"  # widely supported format for H.264
        self.stream.width, self.stream.height = size

    def close(self) -> None:
        """Close the video file."""
        if self.container and self.stream:
            for packet in self.stream.encode():
                self.container.mux(packet)
            self.container.close()
        self.container, self.stream = None, None

    def __enter__(self) -> "VideoWriter":
        """Enter the context manager."""
        if self.container is None or self.stream is None:
            raise RuntimeError(f"Video file '{self._file}' is not opened")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager."""
        self.close()

    def write(self, image: Image.Image) -> None:
        """Write a frame from a PIL.Image.Image."""
        frame = av.VideoFrame.from_image(image)
        for packet in self.stream.encode(frame):
            self.container.mux(packet)

    def from_images(
        self, dir: str | pathlib.Path, pattern: str | None = None
    ) -> None:
        """Write frames from a sequence of image files."""
        dir = pathlib.Path(dir)

        if not dir.exists():
            raise ValueError(f"Directory '{dir}' does not exist")
        if not dir.is_dir():
            raise ValueError(f"'{dir}' is not a directory")

        files = (
            sorted(
                [
                    file
                    for file in dir.iterdir()
                    if file.suffix.lower() in _IMAGE_FILE_SUFFIXES
                ]
            )
            if pattern is None
            else sorted(dir.glob(pattern))
        )

        if not files:
            raise ValueError(f"Image files not found in the directory '{dir}'")

        with Image.open(files[0]) as im:
            self.stream.width, self.stream.height = im.size

        for file in tqdm(
            files,
            total=len(files),
            desc="Converting video from images",
            unit="frame",
        ):
            with Image.open(file) as im:
                image = im.convert("RGB")
                self.write(image)


class Video:
    """Video object to read or write video files."""

    def __init__(
        self, file: str | pathlib.Path, mode: str = "r", **kwargs
    ) -> None:
        """Open a video file."""
        if mode == "r":
            self._video: VideoReader = VideoReader(file)
        elif mode == "w":
            self._video: VideoWriter = VideoWriter(file, **kwargs)
        else:
            raise ValueError(f"Invalid mode '{mode}', must be 'r' or 'w'")

    @classmethod
    def open(
        cls, file: str | pathlib.Path, mode: str = "r", **kwargs
    ) -> "Video":
        """Open a video file."""
        return cls(file, mode, **kwargs)

    def close(self) -> None:
        """Close the video file."""
        self._video.close()

    def __enter__(self) -> VideoWriter | VideoReader:
        """Enter the context manager."""
        return self._video.__enter__()

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        """Exit the context manager."""
        self._video.__exit__(exc_type, exc_val, exc_tb)

    def __getattr__(self, name: str) -> Any:
        """Get the attribute from the video object."""
        if hasattr(self._video, name):
            return getattr(self._video, name)
        raise AttributeError(
            f"'{self.__class__.__name__}' object has no attribute '{name}'"
        )
