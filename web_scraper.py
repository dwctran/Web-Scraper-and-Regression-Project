# Import libraries
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
from selenium.webdriver.edge.options import Options
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

# Create a job scraper function:
# keyword: name of the job
# num_jobs: number of jobs to be scraped
# verbose: show the information of each scrape or not
# path: the path of the webdriver engine
# slp_time: page loading time

def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    """Gathers jobs as a dataframe, scraped from Glassdoor"""

    # Initializing the webdriver, here I choose Edge driver, if you are more of a Chrome person, you can find tutorial on how to use Chrome webdriver on Google.
    service = Service(path)
    options = Options()
    driver = webdriver.Edge(service=service, options=options)

    # The default url for webscraping
    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + keyword + "&sc.keyword" + keyword + "&sc.keyword=" + keyword + "&locT=&locId=&jobType="
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        # Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)
        # time.sleep(.1)

        # Going through each job in this page
        job_buttons = driver.find_elements(by=By.CLASS_NAME, value="react-job-listing")
        
        for job_button in job_buttons:

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))

            if len(jobs) >= num_jobs:
                break

            job_button.click() 

            time.sleep(1)

            collected_successfully = False

            try:
                driver.find_element(by=By.CSS_SELECTOR, value='[alt="Close"]').click()
            except NoSuchElementException:
                pass
            while not collected_successfully:
                try:
                    driver.find_element(by=By.XPATH, value='.//div[@class = "css-t3xrds e856ufb2"]').click()
                    # Get company name
                    company_name = driver.find_element(by=By.XPATH, value='.//div[@class="css-xuk5ye e1tk4kwz5"]').text
                    # Get location
                    location = driver.find_element(by=By.XPATH, value='.//div[@class="css-56kyx5 e1tk4kwz1"]').text
                    # Get job title
                    job_title = driver.find_element(by=By.XPATH,
                                                    value='.//div[contains(@class, "css-1j389vi e1tk4kwz2")]').text
                    # Get job description
                    job_description = [e.text.replace('\n', ' ') for e in
                                       driver.find_elements(by=By.XPATH, value='.//*[contains(@class, "css-1k5huso")]')]
                    collected_successfully = True
                except:
                    time.sleep(5)

            try:
                # Get salary if exists
                salary_estimate = driver.find_element(by=By.XPATH, value='.//span[@class="css-1hbqxax e1wijj240"]').text
            except NoSuchElementException:
                salary_estimate = -1  # You need to set a "not found" value. It's important. You can set to "Unknown" or a NaN value if you wish, as it would be more useful when it comes to data cleaning and exploratory analysis.

            try:
                # Get company rating if exists
                rating = driver.find_element(by=By.XPATH, value='.//span[@class="css-1m5m32b e1tk4kwz4"]').text
            except NoSuchElementException:
                rating = -1  # You need to set a "not found" value. It's important. You can set to "Unknown" or a NaN value if you wish, as it would be more useful when it comes to data cleaning and exploratory analysis.

            # Printing information after each scrape for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))

            # Going to the Company tab...
            # Clicking on this:
            try:
                driver.find_element(by=By.XPATH, value='.//div[@data-item="tab" and @data-tab-type="overview"]').click()
                try:
                    # Get company size if exists
                    size = driver.find_element(by=By.XPATH, value='.//span[text()="Size"]//following-sibling::*').text
                except NoSuchElementException:
                    size = -1 # You need to set a "not found" value. It's important. You can set to "Unknown" or a NaN value if you wish, as it would be more useful when it comes to data cleaning and exploratory analysis.

                try:
                    # Get company's establishment time
                    founded = driver.find_element(by=By.XPATH, value='.//span[text()="Founded"]//following-sibling::*').text
                except NoSuchElementException:
                    founded = -1 # You need to set a "not found" value. It's important. You can set to "Unknown" or a NaN value if you wish, as it would be more useful when it comes to data cleaning and exploratory analysis.

                try:
                    # Get company's type of ownership if exists
                    type_of_ownership = driver.find_element(by=By.XPATH,
value='.//span[text()="Type"]//following-sibling::*').text
                except NoSuchElementException:
                    type_of_ownership = -1 # You need to set a "not found" value. It's important. You can set to "Unknown" or a NaN value if you wish, as it would be more useful when it comes to data cleaning and exploratory analysis.

                try:
                    # Get company's industry
                    industry = driver.find_element(by=By.XPATH,
value='.//span[text()="Industry"]//following-sibling::*').text
                except NoSuchElementException:
                    industry = -1 # You need to set a "not found" value. It's important. You can set to "Unknown" or a NaN value if you wish, as it would be more useful when it comes to data cleaning and exploratory analysis.

                try:
                    # Get company's sector
                    sector = driver.find_element(by=By.XPATH,
value='.//span[text()="Sector"]//following-sibling::*').text
                except NoSuchElementException:
                    sector = -1 # You need to set a "not found" value. It's important. You can set to "Unknown" or a NaN value if you wish, as it would be more useful when it comes to data cleaning and exploratory analysis.

                try:
                    # Get company's revenue
                    revenue = driver.find_element(by=By.XPATH,
value='.//span[text()="Revenue"]//following-sibling::*').text
                except NoSuchElementException:
                    revenue = -1 # You need to set a "not found" value. It's important. You can set to "Unknown" or a NaN value if you wish, as it would be more useful when it comes to data cleaning and exploratory analysis.

            # Rarely, some job postings do not have the "Company" tab.
            except NoSuchElementException:
                # You need to set a "not found" value. It's important. You can set to "Unknown" or a NaN value if you wish, as it would be more useful when it comes to data cleaning and exploratory analysis.
                size = -1
                founded = -1
                type_of_ownership = -1
                industry = -1
                sector = -1
                revenue = -1

            if verbose:
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of Ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            jobs.append({"Job Title": job_title,
                         "Salary Estimate": salary_estimate,
                         "Job Description": job_description,
                         "Rating": rating,
                         "Company Name": company_name,
                         "Location": location,
                         "Size": size,
                         "Founded": founded,
                         "Type of ownership": type_of_ownership,
                         "Industry": industry,
                         "Sector": sector,
                         "Revenue": revenue})
            # add job to jobs

        # Clicking on the "next page" button
        try:
            driver.find_element(by=By.XPATH, value='.//button[@data-test="pagination-next"]').click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  # This converts the dictionary object into a pandas DataFrame.
