from setuptools import setup, find_packages

setup(
    name='issnresolver',
    version='0.1.0',
    description='ISSN ↔ ISSN-L async lookup via ISSN Portal',
    author='Your Name',
    author_email='your@email.com',
    url='https://github.com/yourusername/issnresolver',
    packages=find_packages(),
    install_requires=[
        'aiohttp>=3.8.0',
        'pandas>=1.3.0',
        'tqdm>=4.0.0'
    ],
    python_requires='>=3.8',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'License :: OSI Approved :: MIT License',
    ],
)