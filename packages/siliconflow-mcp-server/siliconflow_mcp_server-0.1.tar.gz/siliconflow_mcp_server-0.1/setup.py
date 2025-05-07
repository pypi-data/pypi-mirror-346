from setuptools import setup

setup(
    name="siliconflow-mcp-server",
    version="0.1",
    packages=["siliconflow_mcp_server"],
    entry_points={
        "console_scripts": [
            "siliconflow-mcp-server=siliconflow_mcp_server.__main__:main",
        ],
    },
)
