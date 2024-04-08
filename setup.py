from setuptools import setup, find_packages

setup(
    name="PyArtistry",
    version="1.0.0",
    author="Marcelo Fonseca Tambalo",
    author_email="marcelozokis@gmail.com",
    packages=find_packages(),
    license="LICENSE.txt",
    description="A Python Library for Creative Coding.",
    long_description=open("README.md").read(),
    install_requires=[
        "Pillow >= 10.3.0",
    ],
)
