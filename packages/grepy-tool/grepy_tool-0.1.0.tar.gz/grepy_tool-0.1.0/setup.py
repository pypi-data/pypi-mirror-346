from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="grepy-tool",  # Must be unique on PyPI
    version="0.1.0",
    author="Prabh-Kesar",
    author_email="lolcodelang@gmail.com",
    description="An enhanced grep-like tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/prabhkesar123/grepy",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "colorama>=0.4.4",
    ],
    entry_points={
        "console_scripts": [
            "grepy=grepy.grepy:main",
        ],
    },
)
