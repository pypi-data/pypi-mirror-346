from setuptools import find_packages, setup

setup(
    name="zeroshotdata",
    version="0.2.3",
    description="Stream zeroshot dataset",
    author="Zeroshot",
    author_email="code@zeroshotdata.com",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "pandas",
        "requests",
        "mosaicml-streaming>=0.11.0",
        "opencv-python",
        "fastparquet>=2024.11.0",
        "gcloud>=0.18.3",
        "google-auth>=2.40.1",
        "google-cloud-storage<2.11.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
)
