from distutils.core import setup

setup(
    name='omr-dataset-tools',
    packages=['omr-dataset-tools'],  # this must be the same as the name above
    version='0.1',
    description='A collection of tools that simplify the downloading and handling of datasets used for Optical Music Recognition (OMR).',
    author='Alexander Pacha',
    author_email='alexander.pacha@tuwien.ac.at',
    url='https://github.com/apacha/omr-datasets',  # use the URL to the github repo
    download_url='https://github.com/apacha/omr-datasets/archive/0.1.tar.gz',
    keywords=['optical music recognition', 'downloading', 'extracting', 'omr', 'generating', 'dataset', 'preprocessing'],
    classifiers=[],
)
