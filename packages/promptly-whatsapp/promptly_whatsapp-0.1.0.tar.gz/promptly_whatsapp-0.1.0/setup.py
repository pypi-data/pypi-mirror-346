from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="promptly-whatsapp",
    version="0.1.0",
    author="Vedank",
    author_email="your.email@example.com",
    description="Send custom prompted messages with beautiful images via WhatsApp automatically",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/itsmeved24/Promptly",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "schedule",
        "pywhatkit",
        "requests",
        "pyautogui",
        "python-dotenv"
    ],
)