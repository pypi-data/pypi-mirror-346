# siliconflow-mcp-server

一个基于 MCP 协议的 SiliconFlow AI API 服务器包，用于集成到支持 MCP 协议的应用程序中。

## 功能特性

- 提供 SiliconFlow 图像生成 API 接口
- 兼容 MCP 协议，可与 Cursor 等工具无缝集成
- 简单易用的工具函数
- 支持通过环境变量配置 API Key

## 安装方法

通过 pip 安装：

```bash
pip install siliconflow_mcp_server
```

通过 uv 安装：

```bash
uvx pip install siliconflow_mcp_server
```

## 使用方法

### 命令行运行

```bash
# 使用普通方式运行
siliconflow-mcp-server

# 使用 uvx 运行
uvx siliconflow-mcp-server
```

### 环境变量配置

在使用前，**必须**设置 SiliconFlow API Key 环境变量：

```bash
export SILICONFLOW_APIKEY="sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
```

你可以从 [SiliconFlow 官网](https://siliconflow.cn) 获取 API Key。

### MCP 配置

在支持 MCP 的应用程序（如 Cursor）中，添加以下配置到 MCP 配置文件中（通常位于 `~/.cursor/mcp.json`）：

```json
{
  "mcpServers": {
    "siliconflow-mcp-server": {
      "command": "uvx",
      "args": [
        "siliconflow-mcp-server"
      ],
      "env": {
        "SILICONFLOW_APIKEY": "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      }
    }
  }
}
```

配置完成后，重启支持 MCP 的应用程序（如 Cursor），即可使用 `@siliconflow-mcp-server` 调用相关工具。

## 可用工具

### 图像生成 (generate_image)

使用 SiliconFlow 的 AI 模型生成图像：

```python
@mcp.tool()
def generate_image(prompt: str, width: int, height: int) -> str:
    """
    根据提示生成图片，返回图片URL
    
    参数:
        prompt: 图片生成的文本提示（必须是英文）
        width: 生成图片的宽度（像素）
        height: 生成图片的高度（像素）
    
    返回:
        生成的图片 URL
    """
```

#### 调用示例

在 Cursor 中，可以这样调用：

```
@siliconflow-mcp-server generate_image("a beautiful landscape with mountains and lakes", 1024, 1024)
```

#### 默认参数

- 使用模型: black-forest-labs/FLUX.1-schnell
- 推理步数: 8
- 指导缩放: 3.5
- 批量大小: 1

## 技术说明

本服务器基于 MCP (Model Control Protocol) 协议，通过 `stdio` 传输方式与客户端通信，可以很容易地与支持 MCP 协议的应用程序集成。

## 开发说明

1. 克隆项目
2. 安装依赖：`pip install -e .`
3. 开发新功能
4. 构建：`python -m build`
5. 发布：`python -m twine upload dist/*`

## 问题排查

- 如果遇到 `ModuleNotFoundError: No module named 'siliconflow_mcp_server'` 错误，请确保已正确安装包
- 如果使用 uvx 运行遇到问题，可以尝试 `uvx pip install --find-links=dist/ siliconflow_mcp_server`

## 许可证

MIT
