from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cmdbapi",  
    version="2.0.1",
    author="Pavlo Lashkevych",
    author_email="laspavel@gmail.com",
    description="A short library for working CMDB API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/laspavel/cmdbapi",
    packages=find_packages(),
    install_requires=['requests>=2.25.1'],
    project_urls={
    'Documentation': 'https://github.com/laspavel/cmdbapi/blob/master/README.md'
    },
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='api cmdb',
    python_requires='>=3.6',
)
