from setuptools import setup, find_packages

setup(
    name="cloud-data-cockpit",
    version="0.1.1",
    description="An interactive interface for selecting and partitioning data with Dataplug.",
    author="Usama",
    author_email="usama.benabdelkrim@urv.cat",
    url="https://github.com/ubenabdelkrim/data_cockpit",
    packages=find_packages(),
    install_requires=[
        "boto3",
        "ipywidgets",
        "gql",
        "dataplug @ git+https://github.com/CLOUDLAB-URV/dataplug",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
