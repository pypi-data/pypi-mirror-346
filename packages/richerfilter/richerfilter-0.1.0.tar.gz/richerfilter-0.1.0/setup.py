from setuptools import setup, find_packages

setup(
    name='richerfilter',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'opencv-python',
        'numpy',
    ],
    entry_points={
        'console_scripts': [
            'richerfilter=richerfilter.filter:process_image',
        ],
    },
)
