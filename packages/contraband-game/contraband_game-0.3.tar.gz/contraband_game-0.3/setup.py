from setuptools import setup, find_packages

setup(
    name="contraband_game",
    version="0.3",  
    packages=find_packages(),
    include_package_data=True,
    package_data={
        "contraband_game": ["data/*.json"]
    },

)


