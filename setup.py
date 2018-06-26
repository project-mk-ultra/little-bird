import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="little-bird",
    version="0.0.2",
    author="ziggs",
    packages=['dht'],
    author_email="ziggs@airmail.cc",
    description="A Python3 Kademlia overlay network implementation. ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ZigmundVonZaun/little-bird",
    # packages=setuptools.find_packages(),
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    install_requires=[
        'python-dotenv',
        'logbook',
        'netifaces'
    ],
)