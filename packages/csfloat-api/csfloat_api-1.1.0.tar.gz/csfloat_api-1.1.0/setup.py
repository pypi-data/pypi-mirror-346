from setuptools import setup, find_packages

setup(
    name='csfloat_api',
    version='1.1.0',
    author='Rushifakami',
    description=(
        'This is an unofficial Python client library for interacting with the '
        'CSFloat API. The library allows users to programmatically access '
        'CSFloat’s listings, buy orders, user information, exchange rates, and more.'
    ),
    packages=find_packages(),
    install_requires=[
        'aiohttp',
        'aiohttp_socks'
    ],
    url='https://github.com/Rushifakami/csfloat_api',
    license='MIT',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    python_requires='>=3.6',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
)