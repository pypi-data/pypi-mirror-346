import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="siliconflow_mcp_server",
    version="0.3.6",
    packages=setuptools.find_packages(),
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'mcp[cli]>=1.3.0',
        'requests>=2.32.3',
        'httpx>=0.28.1',
    ],
    entry_points={
        "console_scripts": [
            "siliconflow-mcp-server=siliconflow_mcp_server.server:main",
        ],
    },
)
