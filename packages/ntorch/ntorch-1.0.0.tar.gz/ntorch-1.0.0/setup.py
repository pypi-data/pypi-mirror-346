from setuptools import setup, find_packages

setup(
    name="ntorch",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "matplotlib>=3.7.0",
        "gym>=0.26.0"
    ],
    author="safe049",
    author_email="safe049@163.com",
    description="A simple PyTorch framework for quick neural network prototyping",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/safe049/ntorch ",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)