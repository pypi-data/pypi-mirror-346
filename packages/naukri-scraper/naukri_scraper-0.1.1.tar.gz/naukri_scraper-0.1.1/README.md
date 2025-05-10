# 🚀 Naukri.com Job Scraper

![Python Version](https://img.shields.io/badge/python-3.6%2B-blue)
![PyPI Version](https://img.shields.io/pypi/v/naukri-scraper?color=green)
![License](https://img.shields.io/badge/license-MIT-green)
![Downloads](https://img.shields.io/pypi/dm/naukri-scraper)

A powerful Python package for scraping job listings from Naukri.com, allowing you to search for jobs by title and collect detailed information in a CSV format. Available as both a command-line tool and a Python library.

## 📋 Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Sample Output](#sample-output)
- [Contributing](#contributing)
- [Connect With Me](#connect-with-me)
- [License](#license)

## ✨ Features

- 🔍 Search for jobs by title on Naukri.com
- 📄 Export job listings to CSV files for easy analysis
- 📊 Extract comprehensive job details including:
  - Job title
  - Company name
  - Job description
  - Company logo URL
  - Experience requirements
  - Job location
  - Posted date
  - Salary information
  - Skills required
  - Job ID and URL
- 📱 User-friendly command-line interface
- 📃 Page navigation functionality

## 📦 Requirements

- Python 3.6+
- `requests` library
- Internet connection

## 💾 Installation

### Using pip (recommended)

```bash
pip install naukri-scraper
```

### From source

```bash
git clone https://github.com/pawankumar941394/naukri-scraper.git
cd naukri-scraper
pip install -e .
```

## 🚀 Usage

### Method 1: Command Line Interface

```bash
# Interactive mode (will prompt for job title and page number)
naukri-scraper

# With command line arguments
naukri-scraper --title "Python Developer" --page 1
```

### Method 2: Python Code - Interactive Mode

```python
from naukri_scraper import scraper

# This will prompt for job title and page number
scraper.main()
```

### Method 3: Python Code - Direct API

```python
from naukri_scraper.scraper import scrape_jobs

# Define job search parameters
job_title = "Data Scientist"
page_number = 1

# Call the function to scrape jobs
result = scrape_jobs(job_title, page_number)

if result:
    job_count, csv_filename = result
    print(f"Found {job_count} jobs matching '{job_title}'")
    print(f"Results saved to: {csv_filename}")
```

### Method 4: Advanced Usage with Data Analysis

```python
import csv
import os
from naukri_scraper.scraper import scrape_jobs

# Get job data
job_title = "Machine Learning"
result = scrape_jobs(job_title, 1)

if result:
    job_count, csv_filename = result
    
    # Example: Analyze the data
    with open(csv_filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        jobs = list(reader)
    
    # Get unique locations
    locations = set()
    for job in jobs:
        if 'Location' in job and job['Location'] != 'N/A':
            locations.add(job['Location'])
    
    print(f"Found jobs in {len(locations)} different locations")
```

## 📁 Package Structure

```
naukri_scraper/
├── __init__.py     # Package initialization
├── scraper.py      # Main scraping functionality
├── headers.py      # Contains headers configuration for HTTP requests
└── cookies.py      # Contains cookies configuration for HTTP requests
```

## 🔧 How It Works

1. The package sends an HTTP request to Naukri.com's API with your search query
2. It uses custom headers and cookies to simulate a browser session
3. The API response is parsed to extract job details
4. Job information is displayed in the terminal and saved to a CSV file
5. The CSV file can be further analyzed using Python's data analysis tools
6. You can search for multiple job titles by running the tool again

## 📊 Sample Output

The script generates a CSV file with the following columns:
- Title
- Company
- Job Description
- Logo URL
- Experience
- Location
- Posted Date
- Salary
- Job ID
- Job URL
- Skills

## 📈 Example Code

See [EXAMPLES.md](EXAMPLES.md) for more detailed examples of how to use this package in your projects.

## 💻 Complete Usage Guide

For a comprehensive guide on installation, usage, and advanced features, see [USAGE_GUIDE.md](USAGE_GUIDE.md).

## 👥 Contributing

Contributions are welcome! Feel free to submit pull requests or open issues to improve this project.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 🔗 Connect With Me

[![YouTube](https://img.shields.io/badge/YouTube-Channel-red?style=for-the-badge&logo=youtube)](https://www.youtube.com/@Pawankumar-py4tk)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Profile-blue?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/pawan941394/)
[![Instagram](https://img.shields.io/badge/Instagram-Profile-purple?style=for-the-badge&logo=instagram)](https://www.instagram.com/p_awan__kumar/)
[![Agency](https://img.shields.io/badge/Our_Agency-Contact_Us-orange?style=for-the-badge&logo=homeadvisor)](https://www.instagram.com/p_awan__kumar/)

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<p align="center">
  <i>Developed with ❤️ by <a href="https://www.youtube.com/@Pawankumar-py4tk">Pawan Kumar</a></i>
</p>
