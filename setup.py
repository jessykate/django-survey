from setuptools import setup, find_packages

setup(
    name="survey",
    version="0.1.1",
    author="Jessy Kate Schingler",
    author_email="jessy@jessykate.com",
    license="AGPL",
    url="https://github.com/jessykate/django-survey",
    packages=find_packages(exclude=[]),
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Affero General Public License v3",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Framework :: Django",
    ]
)
