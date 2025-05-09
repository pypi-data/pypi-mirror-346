from setuptools import setup, find_packages

setup(
    name="snippingtool",
    version="0.1.0",
    description="A simple Python snipping tool using Tkinter and PIL",
    author="RannStudio",
    url="https://github.com/rann-studio/snippingtool",
    project_urls={
        "Source": "https://github.com/rann-studio/snippingtool",
        "Bug Tracker": "https://github.com/rann-studio/snippingtool/issues",
    },
    packages=find_packages(),
    install_requires=[
        "Pillow",
        "pyautogui",
        "pywin32",
    ],
    python_requires='>=3.6',
)
