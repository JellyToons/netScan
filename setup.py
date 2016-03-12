# Author: Sai Uday
from setuptools import setup

_netScan_version = '0.0.1'

install_requires=[
    'pymongo',
    'wget',
    'termcolor',
    'nmap',
    ]

test_requires=[
    'nose'
    ]

setup(
    name = 'netScan',
    version = _netScan_version,
    description = 'Run netScan utility',
    long_description = 'Run portScanning with netScan utility',
    url = 'https://github.com/bhealy/netScan',
    author = '',
    author_email = '',
    license = 'GNU General Public License v2 or later (GPLv2+)',

    classifiers=[
        'Development Status :: 0.0.1-Beta',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Security',
        'Topic :: Software Development :: Security',
        'License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)',
        'Programming Language :: Python :: 2.7',
        'Environment :: Console',
        ],

    keywords='portscanner identifer cpe cpestring NVD vulnerability',
    packages=['netScan'],
    install_requires=install_requires,
    tests_require=test_requires,
    extras_require={
        'tests': install_requires + test_requires,
        },
    package_data = {'netScan': ['*.conf']},

    entry_points={'console_scripts': ['netscan=netscan.netscan:main']},
    test_suite='py.test',
    zip_safe=False,
)
