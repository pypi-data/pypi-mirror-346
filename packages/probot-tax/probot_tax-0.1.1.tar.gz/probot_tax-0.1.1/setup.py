# setup.py

from setuptools import setup, find_packages

setup(
    name='probot_tax',
    version='0.1.1',
    author='Adham Hamdy',
    description='A simple library to calculate ProBot tax only',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/AdhamT1/probot-tax',  # إذا عندك GitHub
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)
