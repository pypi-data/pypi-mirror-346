from setuptools import setup, find_packages

setup(
    name='loglikelihood_estimator',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        'scipy'
    ],
)
