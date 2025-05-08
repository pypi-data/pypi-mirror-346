from setuptools import setup, find_packages

setup(
    
    packages=find_packages(include=['contraband_game']), 
    version = "0.2",
   
    include_package_data=True,
    package_data={
        "contraband_game": ["data/*.json"]
    },
    entry_points={  
        'console_scripts': ['contraband_game=contraband_game.main:main']
    }
    
    
)

