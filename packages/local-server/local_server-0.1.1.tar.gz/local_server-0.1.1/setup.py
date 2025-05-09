from setuptools import setup, find_packages
import subprocess


def parse_requirements(filename):
    with open(filename, encoding="utf-8") as f:
        return f.read().splitlines()


setup(
    name="local-server",
    version="0.1.1",
    author="skyci",
    author_email="your.email@example.com",
    description="A simple FastAPI HTTP server with directory listing",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "local-server=local_server.server:main",
        ],
    },
)
