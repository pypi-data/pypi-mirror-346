from setuptools import setup, find_packages

setup(
    name="pycrea",
    version="0.0.12",
    packages=find_packages(),
    install_requires=[ "scipy", "scikit-learn", "numpy"],  
    include_package_data=True,
    description="A Python package to parse and manage CREA word vectors",
    author="Alex Skitowski",
    author_email="askitowski@mcw.edu",
    url="https://github.com/askitowski1/CREA-Vectors/tree/main/crea_library",
)
 