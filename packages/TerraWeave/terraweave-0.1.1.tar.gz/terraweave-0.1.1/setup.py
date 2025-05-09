from setuptools import setup, find_packages

setup(
    name="TerraWeave",  # Package name
    version="0.1.1",  # Initial version
    description="A Python wrapper for Terraform",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Grant Colgan",
    author_email="grant.colgan@farsetlabs.org.uk",
    url="https://github.com/brains93/TerraWeave",  # Replace with your repo URL
    license="MIT",
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[],  # Add dependencies here if needed
    python_requires=">=3.7",  # Minimum Python version
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            # Add CLI commands if needed, e.g., "pyterra=pyterra.cli:main"
        ]
    },
)