from setuptools import setup, find_packages

setup(
    name='probot_tax',
    version='0.1.3',
    description='A simple library to calculate ProBot tax (5%) with full input handling and output formatting',
    author='Adham Hamdy',
    author_email='example@example.com',
    url='https://github.com/AdhamT1/probot-tax/',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License'
    ],
    python_requires='>=3.6',
)
