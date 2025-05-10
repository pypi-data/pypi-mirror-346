from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="OpenPyLivoxv2",
    version="1.0.2",
    author="Zahid Pichen",
    author_email="zahidpichen1@gmail.com",
    description="Python3 driver for UDP Communications with Livox Lidar sensors ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],    
    python_requires=">=3.6",
    install_requires=[
        "crcmod",
        "numpy",
        "tqdm",
        "laspy",
        "deprecated",
    ],
)
