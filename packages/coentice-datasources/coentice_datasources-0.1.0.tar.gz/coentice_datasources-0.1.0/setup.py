from setuptools import setup, find_packages

setup(
    name="coentice_datasources",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["requests"],
    description="A package for managing datasource templates in Coentice Integration",
    author="Kartik Patel",
    author_email="kartik@prowesolution.com",
)