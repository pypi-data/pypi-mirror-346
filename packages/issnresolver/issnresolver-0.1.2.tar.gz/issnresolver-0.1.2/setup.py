from setuptools import setup, find_packages

setup(
    name='issnresolver',  # keep the same unless renaming on PyPI
    version='0.1.2',      # bump the version (required for metadata changes)

    # Editable fields:
    description='Fast async ISSN ↔ ISSN-L resolver using the ISSN Portal API',
    long_description = open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',

    author='Akmal Setiawan',
    author_email='your@email.com',
    url='https://github.com/acepocalypse/issnresolver',
    project_urls={
        'Source': 'https://github.com/acepocalypse/issnresolver',
        'Tracker': 'https://github.com/acepocalypse/issnresolver/issues',
        'Documentation': 'https://github.com/acepocalypse/issnresolver#readme',
    },

    license='MIT',
    packages=find_packages(),
    python_requires='>=3.8',
    install_requires=[
        'aiohttp>=3.8',
        'pandas>=1.3',
        'tqdm>=4.0',
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ],
)