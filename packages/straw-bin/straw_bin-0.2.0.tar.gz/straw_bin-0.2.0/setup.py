from setuptools import setup, find_packages

setup(
    name='straw-bin',  
    version='0.2.0',
    author='Straw Hat',
    description='A simple package',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),  
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    python_requires='>=3.6',
)