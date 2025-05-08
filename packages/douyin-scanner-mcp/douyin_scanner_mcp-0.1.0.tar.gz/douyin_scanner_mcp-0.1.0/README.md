# Douyin Scanner MCP

抖音账号扫描 MCP 客户端，作为原有 HTTP 服务器的 MCP 包装器，提供 MCP 接口。

## 安装

### 开发模式安装

```bash
# 克隆仓库
git clone https://your-repository-url/douyin-scanner.git
cd douyin-scanner/account_scan/client

# 安装依赖
pip install -e .
```

### 从 PyPI 安装 (一旦发布)

```bash
pip install douyin-scanner-mcp
```

## 使用方法

### 作为 Cursor MCP 工具使用

在 Cursor 的 MCP 配置文件中添加以下配置：

```json
{
  "mcpServers": {
    "douyin-scanner": {
      "command": "uvx",
      "args": [
        "douyin-scanner-mcp"
      ],
      "env": {
        "SERVER_HOST": "127.0.0.1",
        "SERVER_PORT": "8000"
      }
    }
  }
}
```

### 命令行使用

```bash
# 使用 stdio 通信方式运行
douyin-scanner-mcp

# 使用其他通信方式
douyin-scanner-mcp --transport tcp --host 127.0.0.1 --port 9000
```

## 工具列表

该 MCP 客户端提供以下工具：

1. `scan_douyin_account` - 扫描单个抖音账号
2. `scan_multiple_accounts` - 批量扫描多个抖音账号
3. `get_server_info` - 获取服务器信息
4. `get_last_result` - 获取最后一次扫描结果

## 发布到 PyPI

1. 更新版本号 `__version__` in `douyin_scanner_mcp/__init__.py`
2. 构建包：
```bash
python -m build
```
3. 上传到 PyPI：
```bash
python -m twine upload dist/*
```

## 贡献

欢迎提交 Issue 和 Pull Request。

## 许可证

MIT 