"""
Setup file contains package metadata information
"""
from setuptools import setup, find_packages

with open('VERSION', 'r') as file:
    version = file.read()

with open('README.md', 'r') as file:
    long_description = file.read()

with open('requirements.txt') as file:
    requirements = file.read().splitlines()

with open('LICENSE') as file:
    license_text = file.read()

setup(
    name="pypicloud-auth-bitbucket-cloud",
    version=version,
    author='DevOps Team',
    author_email='devops@oblamatik.ch',
    description="Making Bitbucket Cloud authentication accessible for custom pypi cloud.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=requirements,
    license=license_text,
    python_requires=">=3.7",
    include_package_data=True,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Plugins'
        'Intended Audience :: Developers'
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English'
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3.8",
        "Topic :: System :: Systems Administration :: Authentication/Directory",
        "Topic :: Utilities",
        "Typing :: Typed",
    ],
)
