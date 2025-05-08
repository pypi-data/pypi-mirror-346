"""
 htyy
~~~~~~
Version: 0.0.5
"""

from . import client
from . import reponse
from . import extensions
from . import request
from . import version
from . import message
from . import _path
from .windll import windll, platform
from .pyos import *
from .setproctitle_win import setproctitle
from . import pyos, hpyy
from ._infront._htyy_d import (
    combination, cos, cosh, cot, ComplexNumber,
    AdminPrivilegeChecker, exp, sha1, sha224,
    sha256, sha384, sha3_256, sha3_384, sha3_512,
    sha512, shake_128, shake_256, sin, sinh, sqrt,
    factorial, floor, blake2b, blake2s, absolute_value,
    tan, tanh, pi, power, md5, ln, log10, cmd, HF,
    WithHtyy, HtyySet, HtNone, HLen
)
from . import websys, winp
from . import _wallpaper as wallpaper, _h7z as h7z, _system as temsys
import logging, os
from pathlib import Path
import warnings

class HtyyWarning(Warning):
    pass

class HtyyTqdmWarning(HtyyWarning):
    pass

try:
    import tqdm
except:
    warnings.warn(
        "The tqdm library is not detected and some features may be limited. Please run 'pip install tqdm' to install.",
        HtyyTqdmWarning,
        stacklevel=2
    )

__version__ = version.__version__

import miniaudio
import pyaudio
import threading
import time
import numpy as np

class Music:
    def __init__(self, file_path, play_time=-1):
        self.file_path = file_path
        self.play_time = play_time
        self._running = False
        self.audio_thread = None
        self._load_audio()  # 加载音频
        self.play()

    def _load_audio(self):
        """使用 miniaudio 加载音频"""
        try:
            # 解码音频文件（默认输出为 16 位整数）
            decoded = miniaudio.decode_file(self.file_path)
            self.sample_rate = decoded.sample_rate
            self.channels = decoded.nchannels
            # 将数据转换为 numpy 数组（int16）
            self.audio_data = np.frombuffer(decoded.samples, dtype=np.int16)
        except Exception as e:
            raise ValueError(f"Failed to load audio:{e}")

    def _play_audio(self):
        """核心播放逻辑"""
        p = pyaudio.PyAudio()
        stream = p.open(
            format=pyaudio.paInt16,  # 指定 16 位整数格式
            channels=self.channels,
            rate=self.sample_rate,
            output=True
        )

        self._running = True
        start_time = time.time()
        pos = 0
        chunk_size = 1024  # 每次写入的帧数

        while self._running and pos < len(self.audio_data):
            if self.play_time > 0 and (time.time() - start_time) >= self.play_time:
                break

            end_pos = pos + chunk_size * self.channels  # 注意：每个帧包含多个通道的数据
            chunk = self.audio_data[pos:end_pos]
            stream.write(chunk.tobytes())
            pos = end_pos

        stream.stop_stream()
        stream.close()
        p.terminate()

    def play(self):
        if not self._running:
            self.audio_thread = threading.Thread(target=self._play_audio)
            self.audio_thread.start()

    def stop(self):
        self._running = False
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join()

from PIL import Image

class ImageConversionError(Exception):
    """自定义图像转换异常"""
    pass

class ImageConversion:
    SUPPORTED_FORMATS = {
        "jpg": "JPEG",
        "jpeg": "JPEG",
        "png": "PNG",
        "bmp": "BMP",
        "webp": "WEBP",
        "gif": "GIF",
        "tiff": "TIFF"
    }

    def __init__(self, input_path: str, output_path: str, **kwargs):
        """
        初始化图像转换器
        :param input_path:  输入图像路径（如 "D:/input.jpg"）
        :param output_path: 输出图像路径（如 "D:/output.png"）
        :param kwargs:      可选参数（如 quality=85, optimize=True）
        """
        self.input_path = Path(input_path).resolve()
        self.output_path = Path(output_path).resolve()
        self.convert_params = kwargs  # 转换参数（如质量、优化选项）
        self._validate_paths()
        logging.basicConfig(level=logging.INFO)

    def _validate_paths(self):
        """验证输入输出路径合法性"""
        # 输入文件检查
        if not self.input_path.exists():
            raise FileNotFoundError(f"The input file does not exist: {self.input_path}")
        
        # 输入格式支持性检查
        input_ext = self.input_path.suffix.lower()[1:]
        if input_ext not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported input formats: .{input_ext}")

        # 输出目录写入权限检查
        output_dir = self.output_path.parent
        output_dir.mkdir(parents=True, exist_ok=True)
        if not os.access(str(output_dir), os.W_OK):
            raise PermissionError(f"No write permissions: {output_dir}")

        # 输出格式支持性检查
        output_ext = self.output_path.suffix.lower()[1:]
        if output_ext not in self.SUPPORTED_FORMATS:
            raise ValueError(f"Unsupported output formats: .{output_ext}")

    def _get_save_params(self) -> dict:
        """根据输出格式生成保存参数"""
        output_ext = self.output_path.suffix.lower()[1:]
        params = self.convert_params.copy()

        # 格式特定参数（示例：JPEG 质量、PNG 压缩）
        if output_ext in ["jpg", "jpeg"]:
            params.setdefault("quality", 90)  # 默认 JPEG 质量 90%
        elif output_ext == "webp":
            params.setdefault("quality", 80)  # 默认 WEBP 质量 80%
        elif output_ext == "png":
            params.setdefault("compress_level", 6)  # PNG 压缩级别

        return params

    def convert(self):
        """执行图像格式转换"""
        try:
            # 打开输入图像
            with Image.open(self.input_path) as img:
                # 转换 RGBA 格式处理（如 PNG 转 JPEG 需移除透明度）
                if img.mode in ("RGBA", "LA") and self.output_path.suffix.lower() in [".jpg", ".jpeg"]:
                    background = Image.new("RGB", img.size, (255, 255, 255))
                    background.paste(img, mask=img.split()[-1])  # 移除透明度
                    img = background

                # 保存为输出格式
                img.save(
                    self.output_path,
                    format=self.SUPPORTED_FORMATS[self.output_path.suffix.lower()[1:]],
                    **self._get_save_params()
                )
            
            logging.info(f"The conversion was successful: {self.output_path}")

        except IOError as e:
            error_msg = f"Image processing failed: {str(e)}"
            logging.error(error_msg)
            raise ImageConversionError(error_msg)
        except Exception as e:
            logging.error(f"Error: {str(e)}")
            raise

"""
if __name__ == "__main__":
    try:
        converter = VideoConversion(
            input_path="D:/test_video.mp4",
            output_path="D:/output/test_audio.wav"
        )
        converter.convert()
    except Exception as e:
        print(f"转换失败: {str(e)}")
        sys.exit(1)
"""

path = _path
htyy = __file__
import sys
_names = sys.builtin_module_names

if _names == "nt":
    name = "win32"

elif _names == "posix":
    name = "posix"

else:
    name = _names

from ._a import compile_c_to_pyd
_ = name

if __name__ == "__main__":
    setproctitle("TITLE")
    message.showinfo("Title","Message\nmsg")
    response = request.get('https://codinghou.cn', timeout=5)
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text[:200]}...")
    if not path.exists("PATH"):
        pass

    else:
        print(htyy)

    if platform == "windows":
        print("system is windows.")

    elif platform == "linux":
        print("system is linux.")
    
    elif platform == "darwin":
        print("system is macos.")

    else:
        print(platform)