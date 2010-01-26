#! python
from setuptools import setup, find_packages

setup(
    name = "bunch",
    description = "A dot-accessible dictionary (a la JavaScript objects)",
    version = "1.0.0",
    license = 'MIT',
    author = "David Schoonover",
    author_email = "dsc@less.ly",
    long_description = """
        A dot-accessible dictionary (a la JavaScript objects).
    """,
    url = "http://tire.less.ly/hacking/bunch",
    platform = 'Any',
    
    packages=['bunch',],
    zip_safe = True,
    classifiers = [
    ]
)
