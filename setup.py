import setuptools
from setuptools import setup, find_packages


VERSION="0.1.0"

setup_info = dict(
        name="backive",
        version=VERSION,
        author="Marcel M. Otte",
        author_email="qwc+backive@mmo.to",
        url="https://github.com/qwc/backive",
        description="Service for automatic backup of data to disks provided in hot-swap (SATA docking station)",
        license="BSD",
        classifiers=[
            ],
        scripts=[],
        packages=find_packages(),
        setup_requires=[
            "setuptools>=40.4.3",
            "pytest>=3.8.2",
            "pytest_runner>=4.2",
            ],
        install_requires=[
            "jsonschema==2.6.0"
            ],
        tests_require=[
            "pytest_cov>=2.6.0",
            "pytest_pylint>=0.12.3",
            "pytest-pep8>=1.0.6",
            "pylint>=2.1.1",
            "coverage>=4.5.1",
            ]
        )

setup(**setup_info)


