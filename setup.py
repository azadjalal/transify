from setuptools import setup, find_packages

setup(
    name='transify',
    version='1.0.0',
    author='Mohammad Mahdi Azadjalal',
    author_email='mm.azadjalal@gmail.com',
    description='A lightweight Python package designed to facilitate seamless translation for multilingual websites.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/azadjalal/transify',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    python_requires='>=3.6',
    install_requires=[],
    include_package_data=False
)
