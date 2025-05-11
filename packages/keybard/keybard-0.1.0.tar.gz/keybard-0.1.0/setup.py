from setuptools import setup, find_packages

setup(
    name="keybard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pygame>=2.6.0",
        "requests>=2.31.0",
        "setuptools>=42.0.0"
    ],
    description="Librairie Python pour affichage ASCII, son, et mises à jour auto.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
