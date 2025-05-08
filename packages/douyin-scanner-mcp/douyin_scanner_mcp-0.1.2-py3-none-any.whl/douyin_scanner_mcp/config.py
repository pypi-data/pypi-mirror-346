"""
抖音扫描器配置文件
"""
import os
import logging
from pathlib import Path

# 包目录
PACKAGE_DIR = Path(__file__).parent

# 服务相关配置
DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8000

# 浏览器配置
BROWSER_TYPE = os.environ.get("BROWSER_TYPE", "chromium")  # chromium, firefox, webkit
BROWSER_HEADLESS = os.environ.get("BROWSER_HEADLESS", "1") == "1"  # 是否无头模式
BROWSER_TIMEOUT = int(os.environ.get("BROWSER_TIMEOUT", "60000"))

# 抖音扫描配置
DOUYIN_SCAN_MAX_VIDEOS = int(os.environ.get("DOUYIN_SCAN_MAX_VIDEOS", "100"))  # 每个账号最多扫描的视频数量

# 并发限制
CONCURRENT_LIMIT = int(os.environ.get("CONCURRENT_LIMIT", "3"))  # 同时扫描的账号数量限制

# 日志配置
LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# 设置日志
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format=LOG_FORMAT
)

# 创建日志记录器
logger = logging.getLogger("douyin_scanner")

# 从文件加载注入脚本
INJECTION_SCRIPT_PATH = PACKAGE_DIR / "js" / "douyin_items.js"

try:
    if INJECTION_SCRIPT_PATH.exists():
        with open(INJECTION_SCRIPT_PATH, "r", encoding="utf-8") as f:
            DOUYIN_INJECTION_SCRIPT = f.read()
        logger.info(f"已加载抖音注入脚本: {INJECTION_SCRIPT_PATH}")
    else:
        logger.warning(f"抖音注入脚本不存在: {INJECTION_SCRIPT_PATH}")
        DOUYIN_INJECTION_SCRIPT = ""
except Exception as e:
    logger.error(f"加载抖音注入脚本失败: {str(e)}")
    DOUYIN_INJECTION_SCRIPT = ""  # 设置为空字符串作为默认值 