
from setuptools import setup, find_packages

setup(
    name="mseep-mcpvideo",
    version="0.1.0",
    description="Add your description here",
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
    install_requires=['chromadb>=1.0.4', 'colorama>=0.4.6', 'mcp[cli]>=1.6.0', 'smolagents[litellm,mcp]>=1.13.0', 'yfinance>=0.2.55'],
    keywords=["mseep"] + [],
)
