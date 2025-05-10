"""
# ReservoirFlow Setup

## Install:
- Fixed:
    - pip install .
    - python setup.py install
- Listen:
    - pip install --editable .
    - pip install --e .
    - python setup.py develop

## Publish:
0. Install:
    - pip install wheel
    - pip install twine
1. Build:
    - python setup.py bdist_wheel sdist
2. Publish:
    - twine check dist/*
    - twine upload -r testpypi dist/*
    - twine upload dist/*
"""

import re
from pathlib import Path

from setuptools import find_packages, setup

this_directory = Path(__file__).parent
readme = (this_directory / "README.md").read_text(encoding="utf8", errors="ignore")
license = (this_directory / "LICENSE").read_text(encoding="utf8", errors="ignore")
# license = "Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International Public License"

with open("requirements.txt", encoding="utf8", errors="ignore") as f:
    requirements = f.read().splitlines()
    requirements = [r for r in requirements if r[:2] != "-e"]

with open("reservoirflow/__init__.py") as f:
    # version = re.findall("__version__.*(\d.\d.\d).*", f.read())[0]
    version = re.findall('__version__ = "(.*)"', f.read())[0]

setup(
    name="reservoirflow",
    version=version,
    author="Hiesab",
    author_email="contact@hiesab.com",
    maintainer="Zakariya Abugrin",
    maintainer_email="zakariya.abugrin@hiesab.com",
    description="Reservoir Simulation and Engineering Library in Python",
    long_description=readme,
    long_description_content_type="text/markdown",
    # url="https://github.com/hiesabx/reservoirflow",
    # download_url="https://github.com/hiesabx/reservoirflow.git",
    license=license,
    license_files=["LICENSE"],
    keywords=["Petroleum", "Reservoir", "Simulation", "Scientific Computing"],
    project_urls={
        "Website": "https://www.hiesab.com/en/products/reservoirflow/",
        "GitHub": "https://github.com/hiesabx/reservoirflow",
        "Documentation": "https://github.com/hiesabx/reservoirflow",
    },
    python_requires=">=3.8",
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Visualization",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    setup_requires=["pytest-runner"],
    tests_require=["unittest"],
    test_suite="tests",
)
