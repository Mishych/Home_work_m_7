from setuptools import setup, find_namespace_packages

setup(
    name='sort-folder',
    version='0.1.0',
    description='Sorting files',
    author='Mykhailo Tsebak',
    license='MIT',
    packages=find_namespace_packages(),
    entry_points={'console_scripts': ['sort_f = sort_folder.sort:main']}
)