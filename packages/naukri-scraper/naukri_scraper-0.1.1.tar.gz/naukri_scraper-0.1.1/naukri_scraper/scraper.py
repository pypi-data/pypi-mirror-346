"""
Main scraper module for Naukri.com Job Scraper.
"""

import requests
import csv
import urllib.parse
import argparse
from naukri_scraper.headers import headers_naukri
from naukri_scraper.cookies import cookies_naukri


def scrape_jobs(job_title, page_number=1):
    """
    Scrape job listings from Naukri.com based on job title and page number.
    
    Args:
        job_title (str): The job title to search for
        page_number (int): The page number to scrape (default: 1)
        
    Returns:
        tuple: A tuple containing (job_count, csv_filename) or None if failed
    """
    if not job_title:
        print("Job title cannot be empty. Please try again.")
        return None
    
    # URL encode the job title for the search query
    encoded_title = urllib.parse.quote(job_title)
    
    # Create a safe filename based on the job title
    safe_title = job_title.lower().replace(' ', '_').replace('/', '_')
    
    # Define headers based on the request information you provided
    headers = headers_naukri(encoded_title)
    
    # Define cookies - include more from your actual browser session
    cookies = cookies_naukri()
    
    # Use a session to maintain cookies
    session = requests.Session()
    
    print(f"\nSearching for '{job_title}' jobs on Naukri.com...")
    
    # Construct the dynamic URL based on job title
    url = f"https://www.naukri.com/jobapi/v3/search?noOfResults=20&urlType=search_by_keyword&searchType=adv&keyword={encoded_title}&sort=r&pageNo={page_number}&k={encoded_title}&nignbevent_src=jobsearchDeskGNB&seoKey={encoded_title.lower().replace(' ', '-')}-jobs&src=jobsearchDesk&latLong="
    
    # Add the sid parameter to the URL and make the request
    response = session.get(url, headers=headers, cookies=cookies)
    
    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON response
        data = response.json()
        
        # Create filenames based on the search term
        csv_filename = f"naukri_{safe_title}_jobs.csv"
        # Print some basic information about the results
        if "jobDetails" in data:
            job_count = len(data['jobDetails'])
            print(f"\nFound {job_count} job listings for '{job_title}'")
            
            # Create a CSV file to store the job details
            with open(csv_filename, "w", encoding="utf-8", newline='') as f:
                # Use CSV writer to handle escaping properly
                csv_writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
                # Write the header
                csv_writer.writerow(["Title", "Company", "Job Desc","Logo URL", "Experience", "Location", "Posted Date", "Salary", "Job ID", "Job URL", "Skills"])
                # Print details of all jobs
                for i, job in enumerate(data["jobDetails"]):
                    # Get company logo
                    logo_url = job.get('clientLogo', 'N/A')
                    # Fix for the placeholders field (it's a list, not a dictionary)
                    location = "N/A"
                    salary = "N/A"
                    if "placeholders" in job and isinstance(job["placeholders"], list):
                        for placeholder in job["placeholders"]:
                            if placeholder.get("type") == "location":
                                location = placeholder.get("label", "N/A")
                            if placeholder.get("type") == "salary":
                                salary = placeholder.get("label", "N/A")
                                
                    # Get posted date info
                    posted_date = job.get("footerPlaceholderLabel", "N/A")
                    # Get job ID and URL
                    job_id = job.get("jobId", "N/A")
                    job_url = job.get("jdURL", "N/A")
                    # Get skills
                    skills = job.get("tagsAndSkills", "N/A")
                    # Extract job description summary
                    job_desc = job.get("jobDescription", "N/A")
                    
                    
                    print(f"\nJob {i+1}:")
                    print(f"Title: {job.get('title', 'N/A')}")
                    print(f"Company: {job.get('companyName', 'N/A')}")
                    print(f"Logo URL: {logo_url}")
                    print(f"Experience: {job.get('experienceText', 'N/A')}")
                    print(f"Location: {location}")
                    print(f"Salary: {salary}")
                    print(f"Posted: {posted_date}")
                    print(f"Job ID: {job_id}")
                    print(f"Job URL: https://www.naukri.com{job_url}")
                    print(f"Skills: {skills}")
                    print(f"Job Description: {job_desc}")
                    
                    # Write to CSV using csv_writer (handles special characters better)
                    csv_writer.writerow([
                        job.get('title', 'N/A'),
                        job.get('companyName', 'N/A'),
                        job_desc,
                        logo_url,
                        job.get('experienceText', 'N/A'),
                        location,
                        posted_date,
                        salary,
                        job_id,
                        f"https://www.naukri.com{job_url}",
                        skills
                    ])
                    
                    print("-" * 50)
                
            print(f"Job details exported to {csv_filename}")
            return job_count, csv_filename
            
        else:
            print("No job details found in the response")
            with open("response_text.txt", "w", encoding="utf-8") as f:
                f.write(response.text)
            return None
    else:
        print(f"Request failed with status code: {response.status_code}")
        print("Response content:")
        print(response.text)
        with open("error_response.txt", "w", encoding="utf-8") as f:
            f.write(response.text)
        return None


def main():
    """Main function to run the scraper from command line or as an imported module"""
    print("=" * 50)
    print("Naukri.com Job Scraper")
    print("=" * 50)
    
    # Check if being run as a module with argparse
    parser = None
    try:
        # Only create parser when run as script, not when imported
        if __name__ == "__main__":
            parser = argparse.ArgumentParser(description="Scrape job listings from Naukri.com")
            parser.add_argument("--title", "-t", help="Job title to search for")
            parser.add_argument("--page", "-p", type=int, default=1, help="Page number to scrape (default: 1)")
            args = parser.parse_args()
            
            if args.title:
                job_title = args.title
                page_number = args.page
            else:
                # If no arguments provided, use interactive mode
                job_title = input("\nEnter the job title to search: ").strip()
                page_number = input("\nEnter the page number: ").strip() or "1"
        else:
            # Interactive mode when imported as a module
            job_title = input("\nEnter the job title to search: ").strip()
            page_number = input("\nEnter the page number: ").strip() or "1"
    except:
        # Fallback to interactive mode
        job_title = input("\nEnter the job title to search: ").strip()
        page_number = input("\nEnter the page number: ").strip() or "1"
    
    result = scrape_jobs(job_title, page_number)
    
    if result:
        # Ask user if they want to search for another job
        search_again = input("\nWould you like to search for another job? (y/n): ")
        if search_again.lower() == 'y':
            # Call main function again for a new search
            main()


def cli():
    """Entry point for command-line interface"""
    main()


if __name__ == "__main__":
    main()
