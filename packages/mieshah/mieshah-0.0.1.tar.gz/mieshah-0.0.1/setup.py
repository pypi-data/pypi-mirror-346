import setuptools

with open("F:/My Folder/PythonWorkshop/MyPyPi_Packages/package_4/readme.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="mieshah", # Package Name
    version="0.0.1",
    author="Dwaipayan Deb",
    author_email="dwaipayandeb@yahoo.co.in",
    description=" A Python package to calculate light scattering properties/parameters of spherical particles by using Mie theory.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DwaipayanDeb/mieshah",
    packages=setuptools.find_packages(),
    install_requires=[
        'numpy',
        'sympy',
        'dimpy',
        # add other dependencies here
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)