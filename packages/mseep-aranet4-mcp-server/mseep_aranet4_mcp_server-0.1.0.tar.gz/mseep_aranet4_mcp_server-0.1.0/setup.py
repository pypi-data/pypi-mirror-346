
from setuptools import setup, find_packages

setup(
    name="mseep-aranet4-mcp-server",
    version="0.1.0",
    description="Simple MCP server to manage your aranet4 device and local db.",
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
    install_requires=['mcp[cli]>=1.6.0', 'pillow>=11.1.0', 'aranet4>=2.5.1', 'matplotlib>=3.10.1', 'pandas>=2.2.3', 'tzlocal>=5.3.1', 'pyyaml>=6.0.2'],
    keywords=["mseep"] + [],
)
