#/usr/bin/env python

import codecs
import os
import sys

from setuptools import setup, find_packages


if 'publish' in sys.argv:
    os.system('python setup.py sdist upload')
    sys.exit()

read = lambda filepath: codecs.open(filepath, 'r', 'utf-8').read()


# Dynamically calculate the version based on galeria.VERSION.
version = __import__('galeria').get_version()

setup(
    name='django-galeria',
    version=version,
    description='Pluggable gallery/portfolio application for Django projects',
    long_description=read(os.path.join(os.path.dirname(__file__), 'README.rst')),
    author='Guilherme Gondim',
    author_email='semente+django-galeria@taurinus.org',
    maintainer='Guilherme Gondim',
    maintainer_email='semente+django-galeria@taurinus.org',
    license='BSD License',
    url='https://bitbucket.org/semente/django-galeria/',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=['django-imagekit>=2.0.1', 'django-mptt']
)
