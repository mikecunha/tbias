from setuptools import setup, find_packages
# To use a consistent encoding
from codecs import open
from os import path


here = path.abspath(path.dirname(__file__))


def open_file(fname):
    return open(path.join(here, fname), encoding='utf-8')


setup(
    name='tbias',
    version='0.1.0',
    description='Tools for addressing unwanted bias in text data and embeddings.',
    long_description=open_file('README.md').read(),
    url='https://github.com/mikecunha/tbias',
    author='Mike Cunha',
    license=open('LICENSE').read(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Utilities',
        'License :: OSI Approved :: MIT License',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows :: Windows 7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
    keywords='bias, nlp, word embedding, linguistics, WEAT, ethics',
    packages=find_packages(),
    install_requires=['scipy', 'numpy'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    #extras_require={
    #    'dev': ['check-manifest'],
    #    'test': ['coverage'],
    #},

    # If there are data files included in your packages that need to be
    # installed, specify them here. Add small embeddings here?
    # If using Python 2.6 or less, then these have to be included in 
    # MANIFEST.in as well.
    #package_data={
    #    'sample': ['package_data.dat'],
    #},

)
