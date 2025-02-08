from setuptools import setup, find_packages

setup(
    name='ecosloader',
    version='0.0.6',
    description='Bank of Korea ECOS API LOADER',
    author='jaemini.lee',
    author_email='jmlee8939@hanmail.net',
    url='https://github.com/jmlee8939/ecos_api_loader',
    packages=find_packages(include=['ecosloader']),
    install_requires=[
        'requests',
        'pandas',
        'tqdm',
        'selenium',
        'webdriver_manager'
    ]
)