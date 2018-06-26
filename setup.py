import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="torrent-tracker-scraper",
    version="0.0.1",
    author="ziggs",
    packages=['little_bird'],
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
        'pygogo',
        'python-dotenv',
        'logbook',
        'netifaces'
    ],
)