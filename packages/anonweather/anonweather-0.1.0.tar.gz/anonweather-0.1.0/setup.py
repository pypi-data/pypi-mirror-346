from setuptools import setup, find_packages

setup(
    name="anonweather",
    version="0.1.0",
    description="Weather module using api.theanon.xyz API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Amit Ranabhat",
    author_email="ranabhatamit04@gmail,com",
    url="https://api.theanon.xyz",
    packages=find_packages(),
    install_requires=["requests"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License"
    ],
    python_requires='>=3.6',
)
