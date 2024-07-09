# Importing necessary libraries:
from setuptools import setup, find_packages
from typing import List

PKG_NAME = "diamond-price-predictor"
__version__ = "0.0.1"
AUTHOR_USER_NAME = "yuvaneshkm"
AUTHOR_EMAIL = "yuvaneshkm05@gmail.com"
REPO_NAME = "diamond-price-prediction"


def read_file(filepath: str) -> str:
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()


def get_requirements(filepath: str) -> List[str]:
    """This function will return list of all the requirements"""
    with open(filepath, "r") as f:
        content = f.read()
        requirements = content.split("\n")
        if '-e .' in requirements:
            requirements.remove("-e .")
    return requirements


# setup:
setup(
    name=PKG_NAME,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="Diamond Price Predictor",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Trakers": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"
    },
    packages=find_packages(),
    install_requires=get_requirements("requirements_dev.txt"),
)
