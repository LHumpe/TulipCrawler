import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


def _gather_ct_links() -> list[str]:
    # TODO: Implement Database instead of csv files
    scraped_urls = pd.read_csv(
        '/mnt/ShareDrive/Development/Privat/TulipArena/singles/TulipCrawler/local_output/cointelegraph_links.csv')[
        'url'].tolist()

    # Initialize Selenium and Remove Cookie Banner
    driver = webdriver.Chrome(
        executable_path='/mnt/ShareDrive/Development/Privat/TulipArena/singles/TulipCrawler/tulipcrawler/spiders/utils/WebDrivers/chromedriver')
    driver.get("https://cointelegraph.com/tags/bitcoin")
    WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, ".privacy-policy__accept-btn"))).click()

    urls_to_scrape = list()
    iteration = 1
    while True:
        online_urls = [url.get_attribute("href") for url in
                       driver.find_elements_by_css_selector('.post-card-inline__figure-link')]
        new_urls = list(set(online_urls) - set(scraped_urls) - set(urls_to_scrape))

        if not new_urls:
            break
        else:
            urls_to_scrape = urls_to_scrape + new_urls

            print("Found {} new articles after {} iterations.".format(len(urls_to_scrape), iteration))

            WebDriverWait(driver, 20).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, ".posts-listing__more-icon")))
            WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".posts-listing__more-btn"))).click()

        iteration += 1

    driver.close()

    print("Found {} new articles in total. Start scraping...".format(len(urls_to_scrape)))



    return urls_to_scrape
