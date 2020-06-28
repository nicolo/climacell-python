from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="climacell-python",
    version="0.0.7",
    description="Python library to interface with the ClimaCell Weather API",
    py_modules=["climacell_api"],
    packages=find_packages(include=['climacell_api'], exclude=['tests']),
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/nicolo/climacell-python",
    author="Nicolo Giorgi",
    author_email="nicolo.giorgi@gmail.com",
    install_requires=[
            "requests >= 2.0",
            "python-dateutil >= 2.0",
        ],
    extras_require={
        "dev": [
            "pytest >= 5.0",
            "vcrpy >= 4.0",
            ],
    },
)
