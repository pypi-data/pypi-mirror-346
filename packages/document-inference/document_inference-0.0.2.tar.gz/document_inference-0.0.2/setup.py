# setup.py
from setuptools import setup, find_packages

setup(
    name="document-inference",
    version="0.0.2",
    description="Internal Document Analysis Package",
    long_description="Private package accidentally exposed",
    long_description_content_type="text/markdown",
    author="Internal Team",
    author_email="dev@company.com",
    url="https://company-internal.example.com",
    packages=find_packages(),
    include_package_data=True,
    classifiers=["Programming Language :: Python :: 3"],
    python_requires=">=3.6",
)
