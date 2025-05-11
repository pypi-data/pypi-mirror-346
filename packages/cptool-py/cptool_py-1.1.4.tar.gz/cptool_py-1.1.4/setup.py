from setuptools import setup, find_packages

setup(
    name='cptool-py',
    version='1.1.4',
    packages=find_packages(),
    scripts=['cpt', 'cp-tool.py'],
    install_requires=[],
    description='CLI for creating competitive programming problem files',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Simon Ashton',
    author_email='simonashton.dev@gmail.com',
    url='https://github.com/yourusername/cp-tool',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
    ],
)
