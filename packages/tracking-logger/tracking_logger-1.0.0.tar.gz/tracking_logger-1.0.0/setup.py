from setuptools import setup, find_packages
setup(
    name='tracking_logger',
    version='1.0.0',
    packages=find_packages(),
    description='Log parameters, metrics, and artifacts using MLflow.',
    author='Saurav Kumar',
    author_email='Saurav.Kumar@cognizant.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)