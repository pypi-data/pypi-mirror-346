from setuptools import setup, find_packages

setup(
    name="tytodb-pyclient",
    version="0.1.0",
    author="ttd3v",
    description="A TytoDB client for python",
    packages=find_packages(include=["tytodb-client", "tytodb-client.*"]),
    install_requires=[
        "blake3",
        "cffi",
        "cryptography"
    ],
    python_requires=">=3.6",
)
