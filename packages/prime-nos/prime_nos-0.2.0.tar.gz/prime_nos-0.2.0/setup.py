from setuptools import setup, find_packages

setup(
    name="prime_nos",
    version="0.2.0",
    author="Venkatesh",
    description="A simple library to check for prime and coprime numbers",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    license="MIT",
    python_requires=">=3.6",
)
