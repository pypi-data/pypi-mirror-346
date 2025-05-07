
from setuptools import setup, find_packages

setup(
    name="mseep-mcp_remote_macos_use",
    version="0.1.0",
    description="A MCP server for remote MacOS control",
    author="mseep",
    author_email="support@skydeck.ai",
    url="",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=['mcp>=1.4.1', 'python-dotenv>=1.0.1', 'pillow>=10.0.0', 'pyDes>=2.0.1', 'cryptography>=44.0.0', 'anthropic>=0.49.0', 'paramiko>=3.5.1', 'livekit>=1.0.5', 'aiohttp>=3.8.1', 'websockets>=10.0', 'aiortc>=1.3.2', 'livekit-api>=1.0.2'],
    keywords=["mseep"] + [],
)
