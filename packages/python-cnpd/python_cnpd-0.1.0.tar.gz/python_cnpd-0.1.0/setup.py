from setuptools import setup, find_packages

setup(
    name="python-cnpd",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        # List your package dependencies here
    ],
    author="flyingcar06",
    author_email="gbwaghmare66@gmail.com",
    description="A short description of your package",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/gauravw66/cnpd",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)