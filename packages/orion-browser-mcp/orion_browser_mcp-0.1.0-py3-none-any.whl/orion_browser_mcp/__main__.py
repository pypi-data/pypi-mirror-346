"""
主模块入口点
"""

import argparse
import sys

from orion_browser_mcp.config import config, update_config_from_args


def parse_args():
    """解析命令行参数
    
    Returns:
        argparse.Namespace: 解析后的参数
    """
    parser = argparse.ArgumentParser(description='浏览器MCP服务器')
    
    # 基本配置
    parser.add_argument('--vision', action='store_true', help='启用视觉模式')
    parser.add_argument('--headless', action='store_true', help='以无头模式运行浏览器')
    
    args = parser.parse_args()
    return args


def main():
    # 解析命令行参数
    args = parse_args()
    
    # 更新配置
    update_config_from_args(args)
    
    from orion_browser_mcp.server.fast_server import main as fast_main
    fast_main()
        
   


if __name__ == "__main__":
    main() 