from setuptools import setup, find_packages
import os
import re

def get_version():
    try:
        import subprocess
        tag = subprocess.check_output(["git", "describe", "--tags", "--abbrev=0"]).decode().strip()
        # Remove leading 'v' if present
        if tag.startswith('v'):
            tag = tag[1:]
        if re.match(r"^\d+\.\d+\.\d+$", tag):
            return tag
    except Exception:
        pass
    return "0.0.0"

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="whisper_transcriber",
    version=get_version(),
    author="Ranjan Shettigar",
    author_email="theloko.dev@gmail.com",
    description="A library for transcribing audio files using Whisper models",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/COILDOrg/whisper-transcriber",
    packages=find_packages(),
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    install_requires=[
        "torch",
        "numpy",
        "tqdm",
        "librosa",
        "transformers",
        "huggingface_hub",
        "regex",
        "pathlib",
        "concurrent-log-handler",  # For better logging with multiprocessing
        "ffmpeg-python",  # For more robust audio processing capabilities
    ],
    entry_points={
        "console_scripts": [
            "whisper-transcribe=whisper_transcriber.cli:main",
        ],
    },
)
