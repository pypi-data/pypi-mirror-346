from setuptools import setup
from setuptools import find_packages

setup(
    name="ideal6",
    version="1.0.1",
    description="Multi-layer AES encryption library",
    author="GroupIDEAL",
    author_email="idealencryption@gmail.com",
    packages=find_packages(include=["bitcrypt","bitcrypt.*","tests","tests.*"]),
    install_requires=[
        "pycryptodome"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires=">=3.6",
)