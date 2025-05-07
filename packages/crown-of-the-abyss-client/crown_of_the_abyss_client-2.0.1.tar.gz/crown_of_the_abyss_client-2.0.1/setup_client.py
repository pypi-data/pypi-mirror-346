"""
To publish this to PyPi (Assuming you have an account):

 1. python3 setup_client.py sdist bdist_wheel
 2. twine upload dist/*
 3. Enter PyPi username/password
    Enviroment variables for this are:

    TWINE_USERNAME=__token__
    TWINE_PASSWORD=pypi-xxxx
"""

from setuptools import setup, find_packages

setup(
    name="crown_of_the_abyss_client",
    version="2.0.1",
    packages=find_packages(include=['client','client.*']),
    install_requires = [
        "pygame",
        "websockets",
    ],
    package_data={
        'client': ['assets/*.jpg', 'assets/*.png'],
    },
    entry_points={
        "console_scripts": [
           "crown-of-the-abyss-client = client:main",
        ]
    }
)
