import setuptools

setuptools.setup(
    name="siliconflow_mcp_server",
    version="0.3.4",
    packages=setuptools.find_packages(),
    install_requires=[
        'mcp>=1.4.1',
        'requests>=2.32.3',
    ],
    entry_points={
        "console_scripts": [
            "siliconflow-mcp-server=siliconflow_mcp_server.server:main",
        ],
    },
)
