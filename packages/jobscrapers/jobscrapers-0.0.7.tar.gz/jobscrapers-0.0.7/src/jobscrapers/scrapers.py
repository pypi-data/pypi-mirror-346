import os
from bs4 import BeautifulSoup
import json
import logging
import re
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

logger = logging.getLogger('jobscrapers')

class WorkdayScraper:
    """Class to scrape a workday careers page."""

    def __init__(self, driver:webdriver=None):
        """Initialize scraper.
        
        Parameters
        ----------
        driver : selenium.webdriver, default=None
            The webdriver to scrape the site.
        """
        if driver == None:
            # TODO make sure chrome driver works too
            logger.debug('No driver specified for scraper. Initializing default driver.')
            self.__driver = self.__init_firefox_driver()
        else:
            self.__driver = driver

    def __init_firefox_driver(self):
        """Initialize a default firefox driver for the webscraper.
        
        Returns
        -------
        """
        options = webdriver.FirefoxOptions()
        options.add_argument('-headless')
        driver = webdriver.Firefox(options=options)
        return driver


    def __get_next_page_class(self, soup:BeautifulSoup):
        """Get the css class of the next button.
        
        Parameters
        ----------
        soup : bs4.BeautifulSoup
            A beautiful soup object created from the html page to search
            for a next button
        
        Returns
        -------
        str
            The class used for the next button or an empty string if there is
            no next button.
        """
        # Get the nav elements responsible for controlling the page
        for nav in soup.find_all("nav", attrs={'aria-label': 'pagination'}):
            # Check all buttons for a next button
            for button in nav.find_all('button'):
                # TODO improve formatting here
                if (
                        button.has_attr('aria-label') and
                        button['aria-label'] == 'next'
                    ):
                    if button.has_attr('class'):
                        return button['class'][0]
        return ''
    
    def __next_page(self, css_class:str):
        """Move to the next page of jobs.
        
        Parameters
        ----------
        css_class : str
            The css class of the next button.

        Raises
        ------
        ValueError
            If there is no next button associated with the specified css class.
        """
        # Move to the next page if it exists
        page_nav_elements = self.__driver.find_elements(
            By.CSS_SELECTOR, '.' + css_class)
        time.sleep(3)
        for element in page_nav_elements:
            # This check needed because previous and next buttons have the same class
            if element.get_attribute('aria-label') == 'next':
                element.click()
                return
        raise ValueError("Next button specified but not found")

    def scrape(self, url:str, cache_path:str=None):
        """Scrape all pages of a specified workday site.
        
        Parameters
        ----------
        url : str
            The url of the site to scrape.
        cache_path : str, default=None
            The path of the directory to store the scaped html pages.
        """
        logger.info(f'Scraping {url} for positions.')
        page_count = 0
        self.__driver.get(url)
        
        # TODO add error handling
        jobs = []
        while True:
            logger.info(f'Scraping page {page_count + 1}')
            next_class = None
            time.sleep(3) # TODO implement better wait strategy
            # get page html
            html = self.__driver.page_source
            soup = BeautifulSoup(html, features='html.parser')
            page_count += 1

            # save current page
            if cache_path != None:
                with open (
                        os.path.join(cache_path, f'p{page_count}.html'), 
                        'w+', encoding='utf-8') as f:
                    f.write(html)

            # Parse html on the current job listing page 
            job_urls = self.__parse_job_urls(html)
            for job_url in job_urls:
                jobs.append(self.__scrape_job_info(job_url))

            # Check for / navigate to next page
            next_class = self.__get_next_page_class(soup)
            if next_class != '':
                self.__next_page(next_class)
            else:
                logger.info("No next button detected. Scraping complete")
                logger.info(f"Scraped {page_count} pages.")
                break
        
        return jobs

    def __parse_job_urls(self, html:str):
        """Parse a workday page for a list of links to positions

        Parameters
        ----------
        html : str
            The Workday page html content to be parsed.
        
        Returns
        -------
        job_urls : list
            A list of urls to positions posted by the company.
        """

        soup = BeautifulSoup(html, features='html.parser')

        # Get canonical url
        canonical_tag = soup.find('link', attrs={'rel': 'canonical'})
        if canonical_tag == None:
            raise Exception('No canonical link in html detected.')
        assert(canonical_tag.has_attr('href'))
        url = canonical_tag['href']
        base_url = re.search(r'^.*myworkdayjobs.com', url).group()

        # Parse all links to position pages
        job_urls = []
        for job_tag in soup.find_all('a', attrs={'data-automation-id': 'jobTitle'}):
            assert(job_tag.has_attr('href'))
            job_urls.append(base_url + job_tag['href'])

        return job_urls
    
    def __parse_job_seo_tags(self, seo_tags):
        """Parse the SEO tags of a specific job posting"""
        return {
            'title': seo_tags['title'],
            'job_id': seo_tags['identifier']['value'],
            'date': seo_tags['datePosted'],
            'employment_type': seo_tags['employmentType'],
            'description': seo_tags['description'],
            'country': seo_tags['jobLocation']['address']['addressCountry'],
            'city': seo_tags['jobLocation']['address']['addressLocality']
        }

    def __scrape_job_info(self, job_url:str, cache_path:str=None):
        """Scrape information from a specific job page.

        Parameters
        ----------
        url : str
            The url to the page with information about the job.
        cache_path : str, default=None
            The path to the cache where information should be stored.
            Information is not cached if not specified.

        Returns
        -------
        dict
            A dict with information about the position at the page.

        Notes
        -----
            See README.MD for information about dict formatting.
        """
        try: 
            resp = requests.get(job_url)
            assert(resp.status_code == 200)
            soup = BeautifulSoup(resp.content, "html.parser")

            # Get the SEO tags from a position
            seo_script_tag = soup.find('script', attrs={'type': 'application/ld+json'})
            if seo_script_tag != None:
                seo_tags = self.__parse_job_seo_tags(json.loads(seo_script_tag.contents[0]))
                seo_tags['scraped_url'] =  job_url
                seo_tags['scrape_successful'] = True
            else:
                raise Exception(f"No SEO Tags found at {job_url}")
        except:
            seo_tags = {
                'scraped_url': job_url,
                'scrape_successful': False
            }
        return seo_tags
            
        # TODO implement caching. See scraping_urls.ipynb for a start

    def close_driver(self):
        """Close the webdriver used by the scraper."""
        self.__driver.close()