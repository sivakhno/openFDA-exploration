from __future__ import absolute_import

import os
from glob import glob
from setuptools import setup, find_packages


# Declare minimal set for installation
required_packages = [
    "python-dotenv>=0.0.5",
    "pandas>=0.24.2",
    "requests",
        "tinydb"
]

setup(
    name="openFA exploration",
    version="v1",
    description="Training and deploying skills models package based on Amazon SageMaker.",
    packages=find_packages(),
    py_modules=[os.path.splitext(os.path.basename(path))[0]
                for path in glob("src/*.py")],
    author="Sergii Ivakhno",
    url="https://github.com/aws/sagemaker-python-sdk/",
    install_requires=required_packages
    )