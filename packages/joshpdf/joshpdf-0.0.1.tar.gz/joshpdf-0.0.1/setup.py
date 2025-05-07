import setuptools
from pathlib import Path

setuptools.setup(
    name="joshpdf",
    version="0.0.1",
    author="Josh",
    description=Path("README.md").read_text(),
    packages=setuptools.find_packages(exclude=["tests", "data"]),
)