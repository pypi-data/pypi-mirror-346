from setuptools import setup, find_packages

# This setup.py is mainly for backward compatibility.
# Modern Python packaging uses pyproject.toml.
setup(
    name="dcache",
    packages=find_packages(),
    install_requires=[
        "diskcache>=5.0.0",
    ],
)