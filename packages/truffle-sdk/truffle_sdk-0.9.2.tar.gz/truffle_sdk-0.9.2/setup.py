from setuptools import setup, find_packages

setup(
    name="truffle-sdk",
    version="0.9.2",
    description="The SDK for TruffleOS cloud/hardware agents",
    author="Deepshard",
    author_email="accounts@deepshard.org",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "grpcio==1.69.0",
        "grpcio-reflection==1.69.0",
        "protobuf==5.29.3",
        "requests==2.32.3"
    ],
    python_requires=">=3.10",
    setup_requires=["wheel"],
    entry_points={
        "console_scripts": [
            "truffle=truffle.cli:main",
        ],
    },      
)
