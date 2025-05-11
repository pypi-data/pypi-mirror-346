# read the contents of your README file
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name="raidpy",
    version="0.1.7",
    packages=find_packages(),
    package_dir={"raidpy": "raidpy"},
    package_data={
        "raidpy": [],
    },
    data_files=[("raidpy", [])],
    include_package_data=True,
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    author="Shibaji Chakraborty",
    author_email="chakras4@erau.edu",
    maintainer="Shibaji Chakraborty",
    maintainer_email="chakras4@erau.edu",
    license="MIT",
    license_files=["LICENSE"],
    description=long_description,
    long_description=long_description,
    install_requires=[],
    keywords=["python", "HF absorption"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    url="https://github.com/shibaji7/R-AID",
)
