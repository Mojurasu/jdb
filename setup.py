import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jdb",
    version="0.2.0",
    author="Simon Schürrle",
    author_email="info@sitischu.com",
    description="Simple json based database",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mojurasu/jdb",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
)
