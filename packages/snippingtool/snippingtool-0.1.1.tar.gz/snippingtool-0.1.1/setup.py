from setuptools import setup, find_packages
import pathlib

# Baca isi README.md
current_dir = pathlib.Path(__file__).parent
readme_path = current_dir / "README.md"
long_description = readme_path.read_text(encoding="utf-8")

setup(
    name="snippingtool",
    version="0.1.1",
    description="A simple Python snipping tool using Tkinter and PIL",
    long_description=long_description,
    long_description_content_type="text/markdown",
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
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
        "Topic :: Multimedia :: Graphics :: Capture",
        "Intended Audience :: End Users/Desktop",
    ],
    include_package_data=True,
)
