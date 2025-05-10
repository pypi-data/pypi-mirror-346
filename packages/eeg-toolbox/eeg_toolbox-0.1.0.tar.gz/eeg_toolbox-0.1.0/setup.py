from setuptools import setup, find_packages

setup(
    name='eeg_toolbox',
    version='0.1.0',
    description='A simple EEG signal processing toolbox',
    author='Veronika Szabolcsi, Dorka Kecskés, Huba Kukor',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/hubakukor/scipy_proj',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'mne',
        'matplotlib'
    ],
    python_requires='>=3.10',
    classifiers=[
        'Programming Language :: Python :: 3',
        ],
)