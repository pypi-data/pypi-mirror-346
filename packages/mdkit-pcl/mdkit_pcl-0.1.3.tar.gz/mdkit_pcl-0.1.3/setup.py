# setup.py
from setuptools import setup, find_packages

setup(
    name="mdkit-pcl",
    version="0.1.3",
    author="Pengcheng Li",
    author_email="your.email@example.com",
    description="A molecular dynamics simulation toolkit",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/mdkit",
    packages=find_packages(),
    package_data={
        "mdkit": ["templates/*.template"],
    },
    install_requires=[
        "rich",
        "numpy",
        "periodictable",
    ],
    entry_points={
        "console_scripts": [
            "mdkit=mdkit.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)