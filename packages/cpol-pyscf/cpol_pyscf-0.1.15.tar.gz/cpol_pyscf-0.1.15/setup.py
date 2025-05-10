import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cpol_pyscf",
    version="0.1.15",
    author="",
    author_email="mailanoopanair@gmail.com",
    description="A package for calculating molecular moments and polarizabilities using PySCF",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "scipy",
        "pyscf",
        "matplotlib",
        "ase",
    ],
)

