from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="brogcursor",
    version="0.1.2",
    author="Gnanesh",
    author_email="gnaneshbalusa016g@gmail.com",
    description="Precise mouse and keyboard action recorder and replayer",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gnanesh-16/brogcursor",
    project_urls={
        "Bug Tracker": "https://github.com/gnanesh-16/brogcursor/issues",
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