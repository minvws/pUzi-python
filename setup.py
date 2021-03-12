#!/usr/bin/python3
"""pUzi-python installer."""

import os
import re
from setuptools import setup, find_packages


def Requirements():
    """Returns the contents of the requirements.txt file as requirements information."""
    with open(os.path.join(os.path.dirname(__file__), "requirements.txt")) as r_file:
        return r_file.read()


def Description():
    """Returns the contents of the README.md file as description information."""
    with open(os.path.join(os.path.dirname(__file__), "README.md")) as r_file:
        return r_file.read()


def Version():
    """Returns the version of the library as read from the __init__.py file"""
    main_lib = os.path.join(os.path.dirname(__file__), "uweb3", "__init__.py")
    with open(main_lib) as v_file:
        return re.match(".*__version__ = '(.*?)'", v_file.read(), re.S).group(1)


setup(
    name="pUzi",
    version=Version(),
    description="pUzi, python3, Proficient UZI pass reader in python.",
    long_description=Description(),
    long_description_content_type="text/markdown",
    license="European Union Public Licence 1.2 (EUPL 1.2)",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
    author="Jan Klopper",
    author_email="jan@underdark.nl",
    url="https://github.com/minvws/pUzi-python",
    keywords="Uzipas, pUzi",
    packages=find_packages(),
    include_package_data=True,
    install_requires=Requirements(),
    python_requires=">=3.6",
)
