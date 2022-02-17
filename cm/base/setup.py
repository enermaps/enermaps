from setuptools import find_packages, setup

with open("requirements.txt") as fd:
    requirements = fd.readlines()

setup(
    name="BaseCM",
    version="0.0.1",
    author="enermaps devloppers",
    description=(
        "Base module for elements used accross "
        "calculation modules of the enermaps project"
    ),
    packages=find_packages(),
    install_requires=requirements,
    include_package_data=True,
)
