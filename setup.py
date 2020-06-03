import io
import logging
import os
from os.path import abspath, dirname, join

from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

# Read the version from
version_path = join(abspath(dirname(__file__)), 'omrdatasettools', '_version.py')
version_dict = {}
exec(open(version_path, 'r').read(), version_dict)
version_number = version_dict['__version__']


def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)


def get_long_description():
    readme = os.path.join(here, 'README_omrdatasettools.md')
    changes = os.path.join(here, 'CHANGES.md')

    if os.path.isfile(readme) and os.path.isfile(changes):
        long_description = read(readme, changes)
    else:
        logging.warning('Could not find README.md and CHANGES.md file'
                        ' in directory {0}. Contents:'
                        ' {1}'.format(here, os.listdir(here)))
        long_description = 'A collection of tools that simplify the downloading and handling of datasets used for ' \
                           'Optical Music Recognition (OMR).' \
                           'These tools are available as Python package ``omrdatasettools`` on PyPi.' \
                           '' \
                           'They simplify the most common tasks such as downloading and extracting a dataset, ' \
                           'generating images from textual representations or visualizing those datasets. '
    return long_description


setup(
    name='omrdatasettools',
    packages=find_packages('.'),
    version=version_number,
    description='A collection of tools that simplify the downloading and handling of datasets used for Optical Music '
                'Recognition (OMR).',
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author='Alexander Pacha',
    author_email='alexander.pacha@tuwien.ac.at',
    license='MIT',
    url='https://github.com/apacha/omr-datasets',  # use the URL to the github repo
    download_url='https://github.com/apacha/OMR-Datasets/archive/{0}.tar.gz'.format(
        version_number),
    keywords=['optical music recognition', 'downloading', 'extracting', 'omr', 'generating',
              'dataset', 'preprocessing'],
    install_requires=['Pillow', 'muscima', "mung", "numpy", "tqdm", "scikit-image", "lxml"],
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 5 - Production/Stable',

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
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)
