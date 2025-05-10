from setuptools import setup, find_packages

setup(
    name='opeira',
    version='0.0.5',
    author='opeira',
    packages=find_packages(),
    url='http://pypi.python.org/pypi/opeira/',
    license='MIT',
    description='OPEIRA - Energy and Process Systems Toolbox',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    install_requires=[
        # Any dependencies the package might have. Example:
        # "requests >= 2.20.0",
    ],
)
