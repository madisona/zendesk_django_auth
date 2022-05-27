
import os
from setuptools import setup, find_packages

from zendesk_auth import VERSION

README = os.path.join(os.path.dirname(__file__), 'README.rst')
LONG_DESCRIPTION = open(README, 'r').read()
setup(
    name="zendesk_django_auth",
    version=VERSION,
    author="Aaron Madison",
    description="Use your django app as an auth platform for Zendesk.",
    long_description=LONG_DESCRIPTION,
    url="https://github.com/madisona/zendesk_django_auth",
    packages=find_packages(exclude=["example*"]),
    include_package_data=True,
    install_requires=open('requirements/requirements.txt').read().split('\n'),
    tests_require=open('requirements/test.txt').read().split('\n'),
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.2",
        "Framework :: Django :: 4.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
