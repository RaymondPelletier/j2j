"""Setuptools module derived from https://github.com/pypa/sampleproject/blob/d4ee05fdc03e848ed6e7065d8fe8e833a3c8c0b2/setup.py

See:
https://packaging.python.org/guides/distributing-packages-using-setuptools/
https://github.com/pypa/sampleproject
"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="j2j",
    version="0.0.1",  # Required
    description="A minimally viable Python package for processing structured data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="hhttps://github.com/RaymondPelletier/j2j",
    author="Ray Pelletier",  # Optional
    author_email="pelletier+j2j@alumni.cmu.edu",
    classifiers=[  # Optional
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Interpreters",
        "Topic :: Other/Nonlisted Topic",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Other",
        # Pick your license as you wish
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="development, JSON, structured data, pattern matching",  # Optional
    packages=find_packages(where="."),
    python_requires=">=3.6, <4",
    install_requires=["antlr4-python3-runtime"],
    project_urls={
        "Bug Reports": "https://github.com/pypa/sampleproject/issues",
        "Source": "https://github.com/pypa/sampleproject/",
    },
)
