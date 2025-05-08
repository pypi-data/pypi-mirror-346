from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="reverbed",
    version="0.2.0",  # Increment version number from what was shown in README
    author="Param",
    author_email="patelparam0767@gmail.com",  # Replace with your email
    description="A Python package for creating slowed and reverbed versions of videos",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/paramp07/reverbed",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pytube",
        "moviepy",
        "yt-dlp",
        "soundfile",
        "pedalboard",
        "numpy",
    ],
    entry_points={
        "console_scripts": [
            "reverbed=reverbed.cli:main",
        ],
    },
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
            "build",
            "twine",
        ],
        "api": [
            "fastapi",
            "uvicorn",
            "pydantic",
        ],
    },
)
