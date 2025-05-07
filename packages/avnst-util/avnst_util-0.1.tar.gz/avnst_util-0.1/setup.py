from setuptools import setup, find_packages
import os

setup(
    name='avnst_util',
    version='0.1',
    packages=find_packages(),
    description='Avansight Python utility package',
    author='Eric Liu',
    author_email='eric.liu@avansightinc.com',
    install_requires=[
        'pandas>=1.0.0',
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    keywords='clinical trials, data analysis, time alignment, TEAE',
    url='https://github.com/avansightinc/avnst_util',
    long_description=open('README.md').read() if os.path.exists('README.md') else '',
    long_description_content_type='text/markdown',
)
