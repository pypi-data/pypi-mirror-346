from setuptools import setup, find_packages

setup(
    name="cccAPI",  # Name of your package
    version="0.0.3",  # Package version
    description="A Python client for interacting with the CCC API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Aalap Tripathy",
    author_email="atripathy.bulk@gmail.com",
    url="https://github.com/atripathy86/cccAPI",  # Replace with your GitHub repo URL
    license="MIT",  # License type
    packages=find_packages(where="."),  # Automatically find packages in the directory
    install_requires=[
        "requests>=2.25.1",  # Add your dependencies here
        "jsonschema >=4.23.0",
    ],
    python_requires=">=3.6",  # Minimum Python version
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)