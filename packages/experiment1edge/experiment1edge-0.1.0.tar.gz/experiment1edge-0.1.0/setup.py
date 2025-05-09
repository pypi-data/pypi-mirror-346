# setup.py
from setuptools import setup, find_packages

setup(
    name="experiment1edge",
    version="0.1.0",
    author="Akshay",
    description="Edge detection tool using OpenCV",
    packages=find_packages(),
    install_requires=["opencv-python"],
    entry_points={
        "console_scripts": [
            "experiment1edge=experiment1edge.cli:main"
        ]
    },
    python_requires=">=3.6"
)
