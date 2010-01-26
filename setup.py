import os
from distutils.core import setup

version = "1.0.0"

# Read the long description from the README.txt
here = os.path.abspath(os.path.dirname(__file__))
f = open(os.path.join(here, 'README.rst'))
readme = f.read()
f.close()


setup(
    name = "bunch",
    description = "A dot-accessible dictionary (a la JavaScript objects)",
    version = version,
    author = "David Schoonover",
    author_email = "dsc@less.ly",
    long_description = readme,
    url = "http://tire.less.ly/hacking/bunch",
    download_url = "http://pypi.python.org/packages/source/B/bunch/bunch-%s.tar.gz" % version,
    
    packages=['bunch',],
    keywords = ['dict', 'bunch', 'mapping', 'utilities',],
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Utilities',
    ]
    license = 'MIT',
    zip_safe = True,
)

