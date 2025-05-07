from setuptools import setup, find_packages

setup(
    name="playlab-api",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "requests>=2.31.0",
        "ipython>=8.0.0",
    ],
    author="Teaghan O'Briain",
    description="A Python client for the Playlab API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/teaghan/playlab-python",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
) 