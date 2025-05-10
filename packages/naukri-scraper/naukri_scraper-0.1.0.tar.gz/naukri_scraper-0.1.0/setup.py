"""
Setup script for the naukri_scraper package.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="naukri-scraper",
    version="0.1.0",
    author="Pawan Kumar",
    author_email="pawan941394@gmail.com",
    description="A tool for scraping job listings from Naukri.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pawankumar941394/naukri-scraper",
    project_urls={
        "Bug Tracker": "https://github.com/pawankumar941394/naukri-scraper/issues",
        "YouTube Channel": "https://www.youtube.com/@Pawankumar-py4tk",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Indexing/Search",
    ],
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.0.0",
    ],
    entry_points={
        "console_scripts": [
            "naukri-scraper=naukri_scraper.scraper:cli",
        ],
    },
)
