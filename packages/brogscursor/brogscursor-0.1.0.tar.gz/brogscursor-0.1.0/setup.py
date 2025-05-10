from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="brogscursor",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Precise mouse and keyboard action recorder and replayer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/brogscursor",
    project_urls={
        "Bug Tracker": "https://github.com/yourusername/brogscursor/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        "pyautogui>=0.9.53",
        "pynput>=1.7.6",
        "rich>=12.5.0",
    ],
    entry_points={
        "console_scripts": [
            "brogscursor=brogscursor.cli:main",
        ],
    },
    include_package_data=True,
)