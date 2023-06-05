from setuptools import setup, find_packages

__version__ = "0.0.1"

requirements = [
    "cryptography",
]

setup(
    name="pUzi",
    version=__version__,
    description="pUzi, python3, Proficient UZI pass reader in python.",
    license="European Union Public Licence 1.2 (EUPL 1.2)",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: European Union Public Licence 1.2 (EUPL 1.2)",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
    ],
    packages=find_packages(),
    package_dir={"app": "app"},
    package_data={"app": ["templates/saml/html/*.html"]},
    url="https://github.com/minvws/pUzi-python",
    install_requires=requirements,
    extras_require={
        "dev": [
            "black",
            "pylint",
            "bandit",
            "mypy",
            "autoflake",
            "coverage",
            "coverage-badge",
            "pytest"
        ]
    },
)
