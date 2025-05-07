from setuptools import setup, find_packages

setup(
    name='reddit-scraper-tool',
    version="0.1.0",
    author="Inioluwa Adenaike",
    author_email="inioluwadenaike@gmail.com",
    description='A Python package for scraping Reddit user data.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ininike/reddit-scraper',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    install_requires=[
        'aiohttp',
    ],
)