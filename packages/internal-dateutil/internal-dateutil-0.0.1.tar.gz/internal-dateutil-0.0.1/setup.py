from setuptools import setup, find_packages

setup(
    name="internal-dateutil",
    version="0.0.1",
    author="sl4x0",
    author_email="sl4x0@example.com",
    description="Dependency Confusion PoC",
    packages=find_packages(include=["internal_dateutil"]),
    install_requires=[],
)
