import re
from pathlib import Path

from setuptools import setup, find_packages

version = re.search(
    r'__version__\s*=\s*"([^"]+)"',
    Path('leblanc/__init__.py').read_text(encoding='utf-8'),
).group(1)

setup(
    name='leblanc',
    version=version,
    packages=find_packages(exclude=['tests', 'tests.*']),
    install_requires=[
        'pandas>=1.3.0',
        'numpy>=1.20.0',
        'Faker>=18.0.0',
    ],
    extras_require={
        'parquet': ['pyarrow'],
        'dev': ['pytest', 'pyarrow'],
    },
    entry_points={'console_scripts': ['leblanc=leblanc.__main__:main']},
    author='wSanice',
    author_email='wansanice@proton.me',
    description='A Python library to generate various synthetic DataFrames for different business sectors (Tech, Food, Finance, Apparel, forestry, etc.).',
    long_description=Path('README.md').read_text(encoding='utf-8'),
    long_description_content_type='text/markdown',
    url='https://github.com/duck-stein/leblanc',
    license='Apache 2.0',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12',
        'Programming Language :: Python :: 3.13',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis'
    ],
    python_requires='>=3.9',
)
