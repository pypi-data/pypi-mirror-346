import runpy
from setuptools import setup, find_packages
from slg_setup import get_script_files

PACKAGE_NAME = "slg-script-helpers"
version_meta = runpy.run_path("./version.py")
VERSION = version_meta["__version__"]

with open("README.md", "r") as fh:
    long_description = fh.read()

def parse_requirements(filename):
    """Load requirements from a pip requirements file."""
    lineiter = (line.strip() for line in open(filename))
    return [line for line in lineiter if line and not line.startswith("#")]

if __name__ == "__main__":
    setup(
        name="slg-script-helpers",
        version=VERSION,
        packages=find_packages(),
        install_requires=parse_requirements("requirements.txt"),
        author="Steven Gotting",
        author_email="sgotting21@gmail.com",  # Replace with your email
        description="Helper functions for Python scripts including standardized config handling",
        long_description=long_description,
        long_description_content_type="text/markdown",
        url="https://github.com/slgotting/script-helpers",  # Replace with your repository URL
        classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        python_requires=">=3.6",
    )