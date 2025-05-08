# TODO add tests
import jobscrapers.scrapers 

class ArgTests:
    def test_invalid_url(self):
        wd_scraper = jobscrapers.scrapers.WorkdayScraper()
        wd_scraper.scrape('not a valid url')