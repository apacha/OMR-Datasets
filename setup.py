from distutils.core import setup

from setuptools import find_packages

setup(
    name='omrdatasettools',
    packages=find_packages('.'),
    version='0.14',
    description='A collection of tools that simplify the downloading and handling of datasets used for Optical Music Recognition (OMR).',
    author='Alexander Pacha',
    author_email='alexander.pacha@tuwien.ac.at',
    license='MIT',
    url='https://github.com/apacha/omr-datasets',  # use the URL to the github repo
    download_url='https://github.com/apacha/OMR-Datasets/archive/0.14.tar.gz',
    keywords=['optical music recognition', 'downloading', 'extracting', 'omr', 'generating', 'dataset', 'preprocessing'],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',

        'Topic :: Scientific/Engineering :: Image Recognition',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Multimedia :: Graphics',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: MIT License',

        # Specify the Python versions you support here.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
