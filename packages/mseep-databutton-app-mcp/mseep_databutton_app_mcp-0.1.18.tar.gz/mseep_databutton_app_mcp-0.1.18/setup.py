
from setuptools import setup, find_packages

setup(
    name="mseep-databutton-app-mcp",
    version="0.1.18",
    description="Call your Databutton app endpoints as LLM tools with MCP",
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
    install_requires=['certifi>=2025.1.31', 'httpx>=0.28.1', 'websockets>=15.0.1'],
    keywords=["mseep"] + ['databutton', 'app', 'mcp', 'llm', 'tool'],
)
