from setuptools import setup, find_packages
setup(
    name='model_tracking',
    version='1.0.0',
    packages=find_packages(),
    description='Log parameters, metrics, and artifacts using Model Tracking Logger.',
    author='Saurav Kumar',
    author_email='Saurav.Kumar@cognizant.com',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)