import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="asyncpubsub",
    version="0.1.0",
    author="fr0zty",
    author_email="darshn0108@gmail.com",
    description="simple publisher-subscriber for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fR0zTy/asyncpubsub.git",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU GPL3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
