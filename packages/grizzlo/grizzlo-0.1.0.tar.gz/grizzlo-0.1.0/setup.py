from setuptools import setup, find_packages

setup(
    name="grizzlo",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0,<2.0.0",
        "matplotlib>=3.0.0",
        "numpy>=1.18.0"
    ],
    author="Your Name",
    author_email="you@example.com",
    description="High-performance, scalable Pandas-compatible analytics library",
    url="https://github.com/yourname/grizzlo",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)