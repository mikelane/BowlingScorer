import pathlib

from setuptools import setup

# metadata
NAME = 'bowling scorer'
DESCRIPTION = 'Homework for Daily Insights'
URL = 'https://github.com/mikelane/BowlingScorer'
EMAIL = 'self@mikelane.io'
AUTHOR = 'Michael Lane'
REQUIRES_PYTHON = '>=3.7.0'

# Required packages:
REQUIRED = []

here = pathlib.Path(__file__).cwd()

with open(f'{here / "README.md"}', 'r') as f:
    LONG_DESCRIPTION = f'\n{f.read()}'

setup(
    name=NAME,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    py_modules=['bowling_scorer'],
    entry_points={
        'console_scripts': ['bowling_scorer=bowling_scorer:cli'],
    },
    install_requires=REQUIRED,
    include_package_data=True,
    license='MIT',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
    ]
)
