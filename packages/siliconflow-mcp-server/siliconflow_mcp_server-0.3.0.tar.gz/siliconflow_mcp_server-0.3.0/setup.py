from setuptools import setup

setup(
    name="siliconflow-mcp-server",
    version="0.3",
    packages=["siliconflow_mcp_server"],
    install_requires=[
        'mcp>=1.4.1',
        'requests>=2.32.3',
    ],
    entry_points={
        "console_scripts": [
            "siliconflow-mcp-server=siliconflow_mcp_server.__main__:main",
        ],
    },
)
