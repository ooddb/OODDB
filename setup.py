from setuptools import find_packages, setup

setup(
    name="ooddb",
    version="0.1",
    url="https://github.com/ooddb/OODDB",
    packages=find_packages(),
    install_requires=[
        # "numpy",
        "Pillow",
        "torch",
    ],
    package_data={
        "OODDB": ["splits/*/*.json"],
    },
)
