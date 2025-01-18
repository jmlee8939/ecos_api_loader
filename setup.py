from setuptools import setup, find_packages

setup(
    name='ecosloader',
    version='0.0.1',
    packages=find_packages(include=['ecosloader']),
    install_requires=[
        'requests',
        'pandas',
        'tqdm',
        'selenium',
        'webdriver_manager'
    ]
)