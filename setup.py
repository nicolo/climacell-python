from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="climacell-python",
    version="0.0.1",
    description="Python library to interface with the ClimaCell API",
    py_modules=["climacell_api"],
    package_dir={"": "src"},
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    url="https://github.com/judy2k/helloworld",
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
