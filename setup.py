
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
    install_requires=['django>=1.3', 'PyJWT==0.1.5'], # so we can use generic views
    tests_require=["mock"],
    zip_safe=False,
    classifiers = [
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
    ],
)