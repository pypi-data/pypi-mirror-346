from setuptools import setup, find_packages

setup(
    name="ais-toolkit-rohan",
    version="0.1.0",
    description="AIS, Genetic Algorithm, and Ant Colony Optimization toolkit",
    author="Rohan Kaitake",
    author_email="your_email@example.com",
    packages=find_packages(),
    install_requires=[
        "numpy",
        "deap",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
