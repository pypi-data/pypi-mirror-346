from setuptools import setup, find_packages
import os

# Lê o conteúdo do README.md para mostrar no PyPI
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="flydev-mav",
    version='0.6.0',
    author="FlyDev Brasil",
    author_email="contato@flydevbr.com",
    description="Comandos MAVLink em português para controle de drones com pymavlink",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "pymavlink"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Natural Language :: Portuguese (Brazilian)",
        "Topic :: Education",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Interface Engine/Protocol Translator"
    ],
    python_requires=">=3.6",
)
