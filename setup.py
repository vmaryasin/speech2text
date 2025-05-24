import os

from setuptools import find_packages, setup

# Read the requirements from requirements.txt
with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="Speech to text",  # Replace with your actual project name
    version="0.1.0",
    description="Simple speech-to-text application using Whisper and PyAnnote for diarization",
    author="Vladimir Maryasin",
    packages=find_packages(where=".", exclude=["tests*", "*.tests"]),
    py_modules=[
        fname[:-3]
        for fname in os.listdir(".")
        if fname.endswith(".py") and fname != "setup.py"
    ],
    install_requires=requirements,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
