from setuptools import setup, find_packages

setup(
    name="baton",
    version="1.0.2",
    author="Colin Nolan",
    author_email="colin.nolan@sanger.ac.uk",
    packages=find_packages(exclude=["tests"]),
    install_requires=open("requirements.txt", "r").read().splitlines(),
    url="https://github.com/wtsi-hgi/python-baton-wrapper",
    license="LGPL",
    description="Python wrapper for baton.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    test_suite="baton.tests",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.5",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)"
    ]
)
