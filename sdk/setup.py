"""Setup configuration for vaccine_tracker_sdk"""
from setuptools import setup, find_packages

with open("sdk/README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="vaccine-tracker-sdk",
    version="1.0.0",
    author="Manish Sau",
    author_email="manish@example.com",
    description="Official Python SDK for the COVID-19 Vaccine Tracker API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Mmaneesh007/covid-vaccine-tracker",
    packages=find_packages(where="sdk"),
    package_dir={"": "sdk"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "requests>=2.28.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "black>=22.0.0",
        ],
    },
    keywords="covid vaccine api sdk tracker vaccination",
    project_urls={
        "Bug Reports": "https://github.com/Mmaneesh007/covid-vaccine-tracker/issues",
        "Source": "https://github.com/Mmaneesh007/covid-vaccine-tracker",
        "Documentation": "https://github.com/Mmaneesh007/covid-vaccine-tracker/blob/main/API_CLIENT_DOCS.md",
    },
)
