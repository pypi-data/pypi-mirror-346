
from setuptools import setup, find_packages

setup(
    name="mseep-mcp-netsuite",
    version="0.1.0",
    description="NetSuite MCP Server",
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
    install_requires=['mcp[cli]', 'fastapi', 'uvicorn', 'requests', 'python-dotenv', 'pydantic', 'httpx', 'sqlparse>=0.5.3', 'timeout-decorator>=0.5.0'],
    keywords=["mseep"] + [],
)
