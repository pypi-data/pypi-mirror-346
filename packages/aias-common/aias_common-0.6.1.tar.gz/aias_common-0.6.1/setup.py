import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aias_common",
    version="0.6.1",
    author="Gisaïa",
    description="ARLAS AIAS common library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(where="src"),
    python_requires='>=3.10',
    package_dir={'': 'src'},
    install_requires=['ecs_logging']
)
