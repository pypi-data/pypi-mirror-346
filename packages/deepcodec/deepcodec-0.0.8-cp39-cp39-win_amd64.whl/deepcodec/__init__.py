# MUST import the core before anything else in order to initialize the underlying
# library that is being wrapped.


# start delvewheel patch
def _delvewheel_patch_1_10_1():
    import ctypes
    import os
    import platform
    import sys
    libs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'deepcodec.libs'))
    is_conda_cpython = platform.python_implementation() == 'CPython' and (hasattr(ctypes.pythonapi, 'Anaconda_GetVersion') or 'packaged by conda-forge' in sys.version)
    if sys.version_info[:2] >= (3, 8) and not is_conda_cpython or sys.version_info[:2] >= (3, 10):
        if os.path.isdir(libs_dir):
            os.add_dll_directory(libs_dir)
    else:
        load_order_filepath = os.path.join(libs_dir, '.load-order-deepcodec-0.0.8')
        if os.path.isfile(load_order_filepath):
            import ctypes.wintypes
            with open(os.path.join(libs_dir, '.load-order-deepcodec-0.0.8')) as file:
                load_order = file.read().split()
            kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
            kernel32.LoadLibraryExW.restype = ctypes.wintypes.HMODULE
            kernel32.LoadLibraryExW.argtypes = ctypes.wintypes.LPCWSTR, ctypes.wintypes.HANDLE, ctypes.wintypes.DWORD
            for lib in load_order:
                lib_path = os.path.join(os.path.join(libs_dir, lib))
                if os.path.isfile(lib_path) and not kernel32.LoadLibraryExW(lib_path, None, 8):
                    raise OSError('Error loading {}; {}'.format(lib, ctypes.FormatError(ctypes.get_last_error())))


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
