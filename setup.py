#!python
# -*- coding: utf-8 -*-
import re
from os.path import dirname, abspath, join
from setuptools import setup

HERE = abspath(dirname(__file__))
readme = open(join(HERE, 'README.rst')).read()

package_file = open(join(HERE, 'bunch/__init__.py'), 'rU')
__version__ = re.sub(
    r".*\b__version__\s+=\s+'([^']+)'.*",
    r'\1',
    [line.strip() for line in package_file if '__version__' in line].pop(0)
)

setup(
    name="bunch",
    version=__version__,
    description="A dot-accessible dictionary (a la JavaScript objects)",
    long_description=readme,
    url="http://github.com/dsc/bunch",
    author="David Schoonover",
    author_email="dsc@less.ly",
    packages=['bunch', ],
    install_requires=["six >= 1.10.0"],
    keywords=['bunch', 'dict', 'mapping', 'container', 'collection'],
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
