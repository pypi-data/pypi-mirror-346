"""
Python SDK for MetalX Lite (MXLite)[https://github.com/koitococo/mxlite]
提供与服务器交互的工具和类，用于系统部署和管理。
"""

# 导出核心类和函数
from .mxlite import (
    MXLite, MXLiteConfig, MXDRunner, ErrorReason
)

from .utils import (
    get_mxd_path,
    get_mxa_path,
)

# 有条件地导入部署相关模块
try:
    from .deployer import MXADeployer
    __all__ = [
        # mxlite模块
        "MXLiteConfig", "MXLite", "MXDRunner", "ErrorReason",
        # utils模块
        "get_mxd_path", "get_mxa_path",
        # deployer模块
        "MXADeployer"
    ]
except ImportError:
    # 缺少asyncssh依赖时不导入MXADeployer
    __all__ = [
        # mxlite模块
        "MXLiteConfig", "MXLite", "MXDRunner", "ErrorReason",
        # utils模块
        "get_mxd_path", "get_mxa_path",
    ]
