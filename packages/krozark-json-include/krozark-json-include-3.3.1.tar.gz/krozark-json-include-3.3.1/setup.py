import os

import setuptools

from json_include import (
    __version__,
    __author__
)


def read(fname):
   return open(os.path.join(os.path.dirname(__file__), fname)).read()

setuptools.setup(
    name='krozark-json-include',
    version=__version__,
    description='An extension for json_include to support file inclusion',
    long_description=read('README.md'),
    long_description_content_type="text/markdown",
    license="MIT License",
    author=__author__,
    author_email='maxime.barbier1991+json-include@gmail.com',
    url='https://github.com/Krozark/json_include',
    keywords="json include",
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python',
        "Programming Language :: Python :: 3",
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "json-build = json_include.__main__:main"
        ]
    },
    python_requires='>=3.6',
)
