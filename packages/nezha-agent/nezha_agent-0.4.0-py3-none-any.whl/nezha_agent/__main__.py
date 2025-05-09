"""
nezha CLI 入口
"""
import sys

# 导入新路径下的 cli 模块
from .ui.cli.cli import app

if __name__ == "__main__":
    sys.exit(app())
