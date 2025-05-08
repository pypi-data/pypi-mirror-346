# Job Scrapers

This is a project that can pull job listing information from careers pages. Currently there is only support for Workday based careers pages with more support coming soon!

Feel free to use this! (But also try not to be spammy with requests)

## Requirements

- Required python packages (Will be installed when installing from the .whl file)
- WebDriver. This will be specific to your browser. You can download here: https://www.selenium.dev/documentation/webdriver/

## Job Information

Scraped information about a job will be formatted in JSON with the following information:
  
- `scraped_url`: `str`
  - the url that was scraped for information.
- `scrape_successful`: `bool`
  - Whether information was extracted from `scraped_url` successfully. If `False` the following fields may not be added to the job. 
- `title`: `str`
  - The title of the position. E.g. "Software Engineer II"
- `job_id`: `str`
  - The ID of the job. This is a string of numbers and letters.
- `date`: `str`
  - The date the job was posted.
- `employment_type`: `str`
  - Type of employment specified by employer. E.g. "FULL_TIME"
- `description`: `str`
  - A description of the position.
- `country`: `str`
  - The country where the position will be.
- `city`: `str`
  - The city where the position will be.

## Logging
This package makes use of the Logging package for python using a logger with the name `jobscrapers`. By default, events with severity `WARNING` and higher will be printed to `sys.stderr`. Please see the `Logging` documentation for configuring logging for your project. https://docs.python.org/3/howto/logging.html#configuring-logging-for-a-library

