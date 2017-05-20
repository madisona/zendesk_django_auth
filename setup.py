
from setuptools import setup, find_packages

from zendesk_auth import VERSION

setup(
    name="zendesk_django_auth",
    version=VERSION,
    author="Aaron Madison",
    description="Use your django app as an auth platform for Zendesk.",
    long_description=open('README.rst', 'r').read(),
    url="https://github.com/madisona/zendesk_django_auth",
    packages=find_packages(exclude=["example*"]),
    include_package_data=True,
    install_requires=open('requirements/dist.txt').read().split('\n'),
    tests_require=open('requirements/test.txt').read().split('\n'),
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 1.8",
        "Framework :: Django :: 1.9",
        "Framework :: Django :: 1.10",
        "Framework :: Django :: 1.11",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)
