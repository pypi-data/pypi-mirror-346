from setuptools import setup, find_packages

setup(
    name="llamasee",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
    ],
    entry_points={
        "console_scripts": [
            "llamasee=llamasee.cli:main"
        ]
    },
    author="Your Name",
    description="LlamaSee: Data comparison + insight generation package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 