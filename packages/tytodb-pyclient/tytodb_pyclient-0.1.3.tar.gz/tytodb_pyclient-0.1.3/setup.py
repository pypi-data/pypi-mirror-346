from setuptools import setup, find_packages

setup(
    name="tytodb-pyclient",
    version="0.1.3",
    author="ttd3v",
    description="A TytoDB client for python",
    packages=find_packages(include=["tytodb_client", "tytodb_client.*"]),
    install_requires=[
        "blake3",
        "cffi",
        "cryptography",
        "pyzmq"
    ],
    python_requires=">=3.6",
)
