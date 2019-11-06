#!/usr/bin/env python

import setuptools

install_requires = [
    'requests>=2.13.0',
    'websockets'
]

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name="shrimpy_python",
    version="0.0.9",
    author="ShrimpyOfficial",
    author_email="support@shrimpy.io",
    description="The Official Shrimpy API Python Client",
    license="MIT",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shrimpy-dev/shrimpy-python",
    install_requires=install_requires,
    packages=["shrimpy"],
    keywords=[
        'orderbook', 'trade', 'bitcoin', 'ethereum', 
        'BTC', 'ETH', 'client', 'api', 'wrapper',
        'exchange', 'crypto', 'currency', 'trading', 
        'trading-api'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)