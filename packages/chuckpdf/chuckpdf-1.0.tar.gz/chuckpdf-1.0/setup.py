import setuptools
from pathlib import Path

setuptools.setup(
    name="chuckpdf",
    version=1.0,
    long_description=Path("README.md").read_text(),
    # This will look at the project and automatically discover the packages that we have, ignoring "tests" and "data" because they don't include sourcecode:
    packages=setuptools.find_packages(exclude=["tests", "data"])
)
