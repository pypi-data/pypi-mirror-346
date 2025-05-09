from setuptools import setup, find_packages

setup(
    name="safe-return",
    version='1.0.0',
    author="Luka",
    author_email="<luka.m21@hotmail.com>",
    description='Safe return math str',
    long_description=open("README.md").read(),
    long_description_content_type='text/markdown',

    keywords=['math', 'expression'],
    classifiers = [
        "Topic :: Scientific/Engineering :: Mathematics",
        "Development Status :: 5 - Production/Stable",
        "Programming Language :: Python :: 3",
    ],

    license = "MIT License",
    include = ["LICENSE", "README.md"],

    install_requires=[],
    packages=find_packages(),
)
