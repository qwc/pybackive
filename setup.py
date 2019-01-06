import setuptools
from setuptools import setup, find_packages


VERSION="0.1.0"

setup_info = dict(
        name="backive",
        version=VERSION,
        author="Marcel M. Otte",
        author_email="qwc+backive@mmo.to",
        url="tbd",
        description="",
        license="BSD",
        classifiers=[
            ],
        packages=find_packages(),

        )

setup(**setup_info)


