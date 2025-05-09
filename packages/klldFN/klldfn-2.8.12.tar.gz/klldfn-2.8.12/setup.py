requirements = [
    'crayons',
    'py-cord',
    'FortniteAPIAsync==0.1.6',
    'sanic==20.12.0',
    'requests',
    'rich',
    'asyncio',
    'jinja2',
    'aioxmpp>=0.13.3',
    'aioconsole>=0.1.15',
    'pytz>=2024.2'
]

try:
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
except FileNotFoundError:
    pass

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
    
setuptools.setup(
    name="klldFN",
    version="2.8.12",
    author="klld",
    description="klldFN",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://klldFN.xyz",
    packages=['klldFN', 'rebootpy', 'rebootpy.ext.commands'],
    python_requires='>=3.5.3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3.12'
    ],
    install_requires=requirements,
)
