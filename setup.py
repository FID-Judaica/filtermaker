from setuptools import setup

setup(
    name='filtermaker',
    version='0.0',
    author='FID-Judaica, Goethe Universität',
    license='MLP 2.0/EUPL 1.1',
    author_email='a.christianson@ub.uni-frankfurt.de',
    url='https://github.com/FID-Judaica/filtermaker',
    description= 'frameword for creating filters based on properties in text',
    long_description=open('README.rst').read(),
    packages=['filtermaker'],
    # entry_points={'console_scripts': ['']},
)
