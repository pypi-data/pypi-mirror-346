from mcp.server.fastmcp import FastMCP
import argparse
import os

host = "0.0.0.0"
port = 8001
mcp = FastMCP("Echo", host=host, port=port)


@mcp.tool()
def generate_image(prompt: str, width: int, height: int) -> str:
    """
    根据提示生成图片，prompt提示词必须是英文，width和height必须是整数，返回的url中Expires、AccessKeyId、Signature等参数需要全部返回，否则无法访问

    Args:
        prompt (str): 图片生成的文本提示
        width (int): 生成图片的宽度
        height (int): 生成图片的高度

    Returns:
        str: 生成的图片路径或URL
    """
    import requests
    import json

    url = "https://api.siliconflow.cn/v1/images/generations"

    payload = {
        "model": "black-forest-labs/FLUX.1-schnell",
        "prompt": prompt,
        "image_size": f"{width}x{height}",
        "batch_size": 1,
        "num_inference_steps": 8,
        "guidance_scale": 3.5
    }
    headers = {
        "Authorization": "Bearer "+os.environ['SILICONFLOW_APIKEY'],
        "Content-Type": "application/json"
    }

    image_url = ""
    response = requests.request("POST", url, json=payload, headers=headers)
    try:
        object = json.loads(response.text)
        image_url = object["images"][0]["url"]
        print(image_url)
    except Exception as e:
        print(e)
        print(response.text)

    return image_url


def main():
    print("Hello from mcp-siliconflow-server!")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
