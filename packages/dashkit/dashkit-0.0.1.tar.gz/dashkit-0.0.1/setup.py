from setuptools import setup, find_packages

setup(
    name="dashkit",
    version="0.0.1",
    description="Modern, ready-to-use CSS styles for Flask/Django dashboards",
    author="DashKit",
    packages=find_packages(),
    extras_require={
        "driveui": ["driveui>=0.0.0"],
    },
    include_package_data=True,
    license="MIT",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    classifiers=[
        "Framework :: Flask",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: User Interfaces",
        "Operating System :: OS Independent",
    ],
)
