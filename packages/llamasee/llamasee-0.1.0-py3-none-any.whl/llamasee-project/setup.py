from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="llamasee",
    version="0.1.0",
    packages=find_packages(include=['llamasee', 'llamasee.*']),
    install_requires=[
        "pandas>=1.3.0",
        "numpy>=1.20.0",
        "scipy>=1.7.0",
        "openai>=1.0.0",
        "python-dateutil>=2.8.2",
        "pytz>=2020.1",
        "pyyaml>=6.0",
        "tqdm>=4.65.0",
        "scikit-learn>=1.0.0",
    ],
    python_requires=">=3.9",
    author="LlamaSee Team",
    author_email="licensing@llamasee.com",
    description="A framework for data comparison and insight generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="data-analysis, insights, comparison, machine-learning, llm",
    url="https://www.llamasee.com",
    project_urls={
        "Bug Tracker": "https://github.com/llamasee/llamasee/issues",
        "Documentation": "https://www.llamasee.com/docs",
        "License": "https://www.llamasee.com/license",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Information Analysis",
    ],
    include_package_data=True,
    package_data={
        "llamasee": ["plugins/config/*.json", "plugins/config/*.yaml"],
    },
) 