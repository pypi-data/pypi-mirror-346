"""
FangCloud MCP - Model Context Protocol (MCP) 服务器实现，提供与 FangCloud 云存储服务的集成
"""

from .fangcloud import main
from .fangcloud_api import FangcloudAPI

__all__ = ["main", "FangcloudAPI"]
