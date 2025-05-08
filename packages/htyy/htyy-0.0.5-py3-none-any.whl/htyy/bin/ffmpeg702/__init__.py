import os
import subprocess
import shutil
from typing import List, Union

import os
import sys
from typing import Optional

Version = Ver = ver = version = "7.0.2"

def get_ffmpeg_path() -> Optional[str]:
    """获取准确的ffmpeg路径（跨平台兼容）"""
    # 获取当前脚本的绝对路径
    if getattr(sys, 'frozen', False):  # 支持PyInstaller打包后路径
        base_dir = sys._MEIPASS
    else:
        base_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 构建目标路径
    bin_dir = os.path.join(base_dir, 'bin')
    executable = 'ffmpeg.exe' if sys.platform == 'win32' else 'ffmpeg'
    
    # 生成完整路径
    ffmpeg_path = os.path.join(bin_dir, executable)
    
    # 验证路径有效性
    if os.path.isfile(ffmpeg_path) and os.access(ffmpeg_path, os.X_OK):
        return ffmpeg_path
    
    # 备用查找方式
    if shutil.which('ffmpeg'):
        return shutil.which('ffmpeg')
    
    return None

# 使用属性确保路径动态获取
class FFmpegPaths:
    @property
    def ffmpeg_path(self) -> Optional[str]:
        return get_ffmpeg_path()
    
    @property
    def bin_dir(self) -> Optional[str]:
        path = get_ffmpeg_path()
        return os.path.dirname(path) if path else None

ffmpeg_path = FFmpegPaths().ffmpeg_path
Version = Ver = ver = version = "7.0.2"
ffmpeg_path_exe = ffmpeg_path

def addPathToEnvironment(path: str, scope: str = 'user') -> bool:
    """添加路径到环境变量"""
    try:
        path = os.path.normpath(path)
        if not os.path.exists(path):
            return False
            
        current_paths = getEnvironmentPaths()
        if path in current_paths:
            return True

        if scope == 'system' and os.name == 'nt':
            subprocess.call(f'setx /M PATH "%PATH%;{path}"', shell=True)
        else:
            subprocess.call(f'setx PATH "%PATH%;{path}"', shell=True)
        return True
    except Exception:
        return False

def isFFmpegInPath() -> bool:
    """检查FFmpeg是否在环境变量中"""
    return shutil.which('ffmpeg') is not None

def deletePathFromEnvironment(path: str) -> bool:
    """从环境变量删除指定路径"""
    try:
        path = os.path.normpath(path)
        current_paths = getEnvironmentPaths()
        if path in current_paths:
            new_path = os.pathsep.join([p for p in current_paths if p != path])
            os.environ['PATH'] = new_path
            return True
        return False
    except Exception:
        return False

def getEnvironmentPaths() -> List[str]:
    """获取所有环境变量路径列表"""
    return os.environ.get('PATH', '').split(os.pathsep)

def appendToCurrentProcessPath(path: str) -> None:
    """临时添加到当前进程环境变量"""
    path = os.path.normpath(path)
    os.environ['PATH'] = f"{os.environ['PATH']}{os.pathsep}{path}"

def locateExecutable(exe_name: str) -> Union[str, None]:
    """在PATH中查找可执行文件位置"""
    return shutil.which(exe_name)

def validateEnvironmentPath(path: str) -> bool:
    """验证路径是否存在于文件系统"""
    return os.path.exists(os.path.normpath(path))

def isPathInEnvironment(path: str) -> bool:
    """检查指定路径是否已在环境变量中"""
    path = os.path.normpath(path)
    return path in getEnvironmentPaths()

def addMultiplePaths(paths: List[str]) -> int:
    """批量添加多个路径，返回成功添加数量"""
    return sum(1 for p in paths if addPathToEnvironment(p))

def clearAllPaths() -> None:
    """清空PATH环境变量（仅当前进程）"""
    os.environ['PATH'] = ''

def getPathDifferences() -> dict:
    """获取系统PATH与当前进程PATH的差异"""
    system_path = os.environ.get('PATH', '')
    process_path = os.environ['PATH']
    return {
        'system': system_path.split(os.pathsep),
        'process': process_path.split(os.pathsep)
    }

def removeDuplicatePaths() -> int:
    """移除环境变量中的重复路径，返回移除数量"""
    current_paths = getEnvironmentPaths()
    unique_paths = []
    removed = 0
    for p in current_paths:
        if p not in unique_paths:
            unique_paths.append(p)
        else:
            removed += 1
    os.environ['PATH'] = os.pathsep.join(unique_paths)
    return removed

def backupEnvironmentVariables() -> dict:
    """备份当前环境变量"""
    return dict(os.environ)

def restoreEnvironmentVariablesFromBackup(backup: dict) -> None:
    """从备份恢复环境变量"""
    os.environ.clear()
    os.environ.update(backup)

def checkPathValidity(path: str) -> bool:
    """检查路径是否有效且可访问"""
    try:
        return os.access(path, os.F_OK | os.R_OK)
    except Exception:
        return False

def getSystemUserPathDiff() -> dict:
    """获取系统路径和用户路径的差异（Windows特有）"""
    if os.name != 'nt':
        return {}
    
    system_path = os.environ.get('Path', '')
    user_path = subprocess.check_output(
        'reg query HKCU\Environment /v Path',
        shell=True,
        text=True
    ).split()[-1]
    return {
        'system': system_path.split(os.pathsep),
        'user': user_path.split(os.pathsep)
    }

def installFFmpegToPath() -> bool:
    """将当前ffmpeg路径添加到环境变量"""
    ffmpeg_dir = os.path.dirname(ffmpeg_path_exe)
    if not os.path.exists(ffmpeg_dir):
        return False
    return addPathToEnvironment(ffmpeg_dir)

def temporaryAddFFmpeg() -> None:
    """临时添加FFmpeg到当前进程PATH"""
    ffmpeg_dir = os.path.dirname(ffmpeg_path_exe)
    appendToCurrentProcessPath(ffmpeg_dir)

def checkFFmpegAvailability() -> bool:
    """综合检查FFmpeg是否可用"""
    if isFFmpegInPath():
        return True
    if os.path.exists(ffmpeg_path_exe):
        return True
    return False

def showPathHierarchy() -> dict:
    """显示环境变量路径的层级结构"""
    paths = getEnvironmentPaths()
    return {
        "Total Paths": len(paths),
        "Valid Paths": sum(1 for p in paths if os.path.exists(p)),
        "Invalid Paths": [p for p in paths if not os.path.exists(p)],
        "Executable Found": {
            'ffmpeg': locateExecutable('ffmpeg'),
            'ffprobe': locateExecutable('ffprobe')
        }
    }