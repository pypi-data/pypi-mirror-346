from setuptools import setup, find_packages

setup(
    name="driveui",
    version="0.0.0",
    description="DashKit Framework Modern Dark Theme",
    author="DashKit",
    packages=find_packages(),
    include_package_data=True,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Framework :: Flask",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)