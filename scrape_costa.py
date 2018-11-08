from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import re


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit visitcostarica.herokuapp.com
    url = "https://visitcostarica.herokuapp.com/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    temps = str(soup.find_all("strong"))
    min_max = re.findall(r'\d+', temps)
    min_temp = min_max[0]
    max_temp = min_max[1]

    # BONUS: Find the src for the sloth image
    sloth_img = soup.find("img", attrs={"alt":"Image 2"})
    sloth_img = url + sloth_img["src"]

    # Store data in a dictionary
    costa_data = {
        "sloth_img": sloth_img,
        "min_temp": min_temp,
        "max_temp": max_temp
    }

    # Quite the browser after scraping
    browser.quit()

    # Return results
    return costa_data
