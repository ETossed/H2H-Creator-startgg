import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="H2H-Creator-startgg",
    version="0.0.0.1",
    author="ETossed",
    author_email="jthroughs@gmail.com",
    description="H2H Spreadsheet Creator for startgg",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ETossed/H2H-Creator-Startgg",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['requests', 'csv']
)