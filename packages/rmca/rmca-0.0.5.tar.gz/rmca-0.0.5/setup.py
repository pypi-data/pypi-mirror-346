from setuptools import setup, find_packages

setup(
    name='rmca',
    version='0.0.5',
    author='rmca',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/rmca/',
    license='MIT',
    description='Rapid Monte Carlo Analysis',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        # Any dependencies the package might have. Example:
        # "requests >= 2.20.0",
    ],
)
