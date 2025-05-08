"""
URL标准化功能测试脚本
"""
import sys
import os
from pathlib import Path

# 添加项目根目录到Python路径
TEST_DIR = Path(__file__).parent
PROJECT_ROOT = TEST_DIR.parent
sys.path.insert(0, str(PROJECT_ROOT))

from douyin_scanner_mcp.scanner import normalize_douyin_url

def test_normalize_url():
    """测试不同格式URL的标准化处理"""
    test_cases = [
        # 原始URL, 期望结果
        (
            "https://www.douyin.com/user/MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv?from_tab_name=main&vid=7501641578822290740",
            "https://www.douyin.com/user/MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv"
        ),
        # 移除查询参数
        (
            "https://www.douyin.com/user/MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv?vid=123456",
            "https://www.douyin.com/user/MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv"
        ),
        # 补全协议
        (
            "www.douyin.com/user/MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv",
            "https://www.douyin.com/user/MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv"
        ),
        # 不完整协议
        (
            "//www.douyin.com/user/MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv",
            "https://www.douyin.com/user/MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv"
        ),
        # 不完整域名
        (
            "douyin.com/user/MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv",
            "https://www.douyin.com/user/MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv"
        ),
        # 只有ID
        (
            "MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv",
            "https://www.douyin.com/user/MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv"
        ),
        # 其他格式URL（不包含/user/）
        (
            "https://www.douyin.com/MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv",
            "https://www.douyin.com/user/MS4wLjABAAAAyyMzuTevpZ1B1hWtbHsg9CroNZlrh5uCQ9aqGKJoKW--j2AUNRCoeDnYjCxDOBwv"
        ),
    ]
    
    for i, (input_url, expected_url) in enumerate(test_cases):
        result = normalize_douyin_url(input_url)
        assert result == expected_url, f"测试用例 {i+1} 失败: 输入 '{input_url}' 得到 '{result}' 而不是期望的 '{expected_url}'"
        print(f"测试用例 {i+1} 通过: {input_url} -> {result}")

if __name__ == "__main__":
    print("开始测试URL标准化功能...")
    test_normalize_url()
    print("所有测试通过!") 