#!python3

import sys

import pkg_resources
import setuptools

MIN_VERSION = "46.0"  # Minimum version for SetupTools

try:
    pkg_resources.require(f"setuptools>={MIN_VERSION}")
except pkg_resources.VersionConflict:
    print(f"Error: version of setuptools is too old (<{MIN_VERSION})!")
    sys.exit(1)

if __name__ == "__main__":
    setuptools.setup(packages=["demo"])
