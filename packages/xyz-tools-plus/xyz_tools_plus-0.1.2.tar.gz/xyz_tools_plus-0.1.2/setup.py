from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='xyz_tools_plus',
    version='0.1.2',
    packages=find_packages(),
    install_requires=[
    ],

    author='mly, wyy, sty',
    description='一个用于多功能的Python库',
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
)