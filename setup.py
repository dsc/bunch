#!/usr/bin/env python
# coding: utf-8


from setuptools import setup


exec(open('neobunch/version.py').read())  # load __version__


setup(
    name="neobunch",
    version=__version__,  # NOQA
    description="A dot-accessible dictionary (à la JavaScript objects)",
    long_description=open("README.rst").read(),
    url="https://github.com/F483/neobunch",
    author="David Schoonover",
    author_email="dsc@less.ly",
    maintainer="Fabian Barkhau",
    maintainer_email="fabian.barkhau@gmail.com",
    packages=['neobunch', ],
    install_requires=open("requirements.txt").readlines(),
    tests_require=open("test_requirements.txt").readlines(),
    keywords=[
        'neobunch', 'bunch', 'dict', 'mapping', 'container', 'collection'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.0",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
    ],
    license='MIT',
)
