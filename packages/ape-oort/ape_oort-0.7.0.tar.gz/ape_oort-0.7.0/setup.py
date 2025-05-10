#!/usr/bin/env python
from setuptools import find_packages, setup

extras_require = {
    "test": [
        "pytest>=6.0",
        "pytest-xdist",
        "pytest-cov",
        "hypothesis>=6.2.0,<7.0",
    ],
    "lint": [
        "black>=24.10.0,<25",
        "mypy>=1.13.0,<2",
        "types-setuptools",
        "types-requests",
        "flake8>=7.1.1,<8",
        "flake8-breakpoint>=1.1.0,<2",
        "flake8-print>=5.0.0,<6",
        "flake8-pydantic",
        "flake8-type-checking",
        "isort>=5.13.2,<6",
        "mdformat>=0.7.19",
        "mdformat-gfm>=0.3.5",
        "mdformat-frontmatter>=0.4.1",
        "mdformat-pyproject>=0.0.2",
    ],
    "release": [
        "setuptools>=75.6.0",
        "wheel",
        "twine",
    ],
    "dev": [
        "commitizen",
        "pre-commit",
        "pytest-watch",
        "IPython",
        "ipdb",
    ],
}

# Combine extras
extras_require["dev"] = (
    extras_require["test"]
    + extras_require["lint"]
    + extras_require["release"]
    + extras_require["dev"]
)

with open("README.md") as readme:
    long_description = readme.read()

setup(
    name="ape_oort",
    version="0.7.0",
    description="ape_oort: Ape Worx Plugin Ecosystem for OORT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Novacypher",
    author_email="novacypher@oortech.com",
    url="https://github.com/novacypher5/ape-oort/",
    include_package_data=True,
    install_requires=[],
    python_requires=">=3.9,<4",
    extras_require=extras_require,
    py_modules=["ape_oort"],
    license="Apache-2.0",
    zip_safe=False,
    keywords="ethereum",
    packages=find_packages(exclude=["tests", "tests.*"]),
    package_data={"ape_oort": ["py.typed"]},
    entry_points={
        "ape.plugins": [
            "oort = ape_oort",
        ],
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
)
