# -*- coding:utf-8 -*-
from setuptools import setup, find_packages
__version__ = '0.1.0.6'

setup(
    name="qinglong-app-sdk",
    version=__version__,
    author="xx299x",
    author_email="xx299x@gmail.com",
    description="QingLong App SDK",
    long_description="",
    long_description_content_type="text/markdown",
    license="BSD",
    keywords="QingLong",
    url="https://github.com/xx299x/qinglong-app-sdk",
    include_package_data=True,
    packages=find_packages(),
    zip_safe=False,
    install_requires=[
        'loguru',
        'requests',
    ],
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Development Status :: 4 - Beta",
        "Topic :: Utilities",
        "License :: OSI Approved :: BSD License",
    ],
    python_requires='>=3.6'
)
