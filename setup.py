from setuptools import setup
from os import path

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(

    name='EES_connector',
    version='1.0.0',
    license='GNU GPLv3',

    author='Pietro Ungar',
    author_email='pietro.ungar@unifi.it',

    description='Tools for launching EES calculation and retrieving results from python',
    long_description=long_description,
    long_description_content_type='text/markdown',

    url='https://www.dief.unifi.it/vp-177-serg-group-english-version.html',
    download_url='https://github.com/SERGGroup/EESConnector/archive/refs/tags/0.2.5.tar.gz',

    project_urls={

        'Source': 'https://github.com/SERGGroup/EESConnector',
        'Tracker': 'https://github.com/SERGGroup/EESConnector/issues',

    },

    packages=[

        'EESConnect'

    ],

    install_requires=[

        'pywin32'

    ],

    classifiers=[

        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',

      ]

)
