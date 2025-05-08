# MUST import the core before anything else in order to initialize the underlying
# library that is being wrapped.


# start delvewheel patch
def _delvewheel_patch_1_10_1():
    import os
    if os.path.isdir(libs_dir := os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'deepcodec.libs'))):
        os.add_dll_directory(libs_dir)


_delvewheel_patch_1_10_1()
del _delvewheel_patch_1_10_1
# end delvewheel patch

from deepcodec._core import time_base, library_versions, ffmpeg_version_info

# Capture logging (by importing it).
from deepcodec import logging

# For convenience, import all common attributes.
from deepcodec.about import __version__
from deepcodec.audio.codeccontext import AudioCodecContext
from deepcodec.audio.fifo import AudioFifo
from deepcodec.audio.format import AudioFormat
from deepcodec.audio.frame import AudioFrame
from deepcodec.audio.layout import AudioLayout
from deepcodec.audio.resampler import AudioResampler
from deepcodec.audio.stream import AudioStream
from deepcodec.bitstream import BitStreamFilterContext, bitstream_filters_available
from deepcodec.codec.codec import Codec, codecs_available
from deepcodec.codec.context import CodecContext
from deepcodec.codec.hwaccel import HWConfig
from deepcodec.container import open
from deepcodec.format import ContainerFormat, formats_available
from deepcodec.packet import Packet
from deepcodec.error import *  # noqa: F403; This is limited to exception types.
from deepcodec.video.codeccontext import VideoCodecContext
from deepcodec.video.format import VideoFormat
from deepcodec.video.frame import VideoFrame
from deepcodec.video.stream import VideoStream
from deepcodec.vfast import VideoReader, InterleavedVideoReader


__all__ = (
    "__version__",
    "time_base",
    "ffmpeg_version_info",
    "library_versions",
    "AudioCodecContext",
    "AudioFifo",
    "AudioFormat",
    "AudioFrame",
    "AudioLayout",
    "AudioResampler",
    "AudioStream",
    "BitStreamFilterContext",
    "bitstream_filters_available",
    "Codec",
    "codecs_available",
    "CodecContext",
    "open",
    "ContainerFormat",
    "formats_available",
    "Packet",
    "VideoCodecContext",
    "VideoFormat",
    "VideoFrame",
    "VideoStream",
    "VideoReader"
    "InterleavedVideoReader"
)


def get_include() -> str:
    """
    Returns the path to the `include` folder to be used when building extensions to av.
    """
    import os

    # Installed package
    include_path = os.path.join(os.path.dirname(__file__), "include")
    if os.path.exists(include_path):
        return include_path
    # Running from source directory
    return os.path.join(os.path.dirname(__file__), os.pardir, "include")
