from setuptools import setup, find_packages

setup(
    name='mathkat',
    version='1.2.0',
    description='Una librería de gradientes para Python con impresión bonita en terminal.',
    author='Fernando Leon Franco',
    packages=find_packages(),
    python_requires='>=3.10',
    install_requires=[
        'numpy>=2.0.0',
        'rich>=13.0.0'
    ],
)