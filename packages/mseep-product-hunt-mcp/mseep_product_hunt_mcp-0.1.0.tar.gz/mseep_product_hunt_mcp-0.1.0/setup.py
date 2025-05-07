
from setuptools import setup, find_packages

setup(
    name="mseep-product-hunt-mcp",
    version="0.1.0",
    description="Product Hunt MCP Server - A FastMCP implementation for the Product Hunt API",
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
    install_requires=['fastmcp>=0.3.0', 'requests>=2.31.0'],
    keywords=["mseep"] + ['mcp', 'product-hunt', 'fastmcp', 'api', 'ai'],
)
