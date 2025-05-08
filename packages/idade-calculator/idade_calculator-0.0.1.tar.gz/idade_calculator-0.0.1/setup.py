from setuptools import setup, find_packages

with open("README.md", "r") as f:
    page_description = f.read()

with open("requirements.txt") as f:
    requirements = f.read().splitlines()

setup(
    name="idade_calculator",
    version="0.0.1",
    author="Fabriciano",
    author_email="fgs85@live.com",
    description="Calculadora de Idade",
    long_description=page_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FabricianoGiovanelli/simple-package-template.git",
    packages=find_packages(),
    install_requires=requirements,
    python_requires='>=3.8'
)