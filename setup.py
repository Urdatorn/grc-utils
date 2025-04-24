from setuptools import setup, find_packages

setup(
    name="grc-utils",                 # Package name
    version="0.2.0",                   # Initial version
    packages=find_packages(),          # Automatically find packages
    install_requires=[                 # Dependencies
        "numpy>=1.21.0",               # Example dependency
    ],
    author="Albin Ruben Johannes Thörn Cleland",
    author_email="albin.thorn_cleland@klass.lu.se",
    description="NLP utilities for Ancient Greek",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Urdatorn/grc-utils",  # GitHub repo URL
    classifiers=[                      # Metadata
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)