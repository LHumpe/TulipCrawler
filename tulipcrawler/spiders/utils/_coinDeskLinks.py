import pandas as pd
import requests


def _gather_cd_links() -> list[str]:
    # TODO: Implement Database instead of csv files
    scraped_urls = pd.read_csv(
        '/mnt/ShareDrive/Development/Privat/TulipArena/singles/TulipCrawler/local_output/coindesk_links.csv')[
        'url'].tolist()

    tags = ['bitcoin-miners', 'markets-bitcoin', 'bitcoin-mining', 'bitcoin-price', 'bitcoin']

    urls_to_scrape = list()
    for search_tag in tags:
        iteration = 0
        while True:
            resp = requests.get(
                'https://www.coindesk.com/wp-json/v1/articles/tag/{}/{}?mode=list'.format(search_tag, iteration)
            )
            try:
                web_posts = resp.json()['posts']
            except KeyError:
                break

            online_urls = ['https://www.coindesk.com/{}'.format(web_post['slug']) for web_post in web_posts]
            new_urls = list(set(online_urls) - set(scraped_urls) - set(urls_to_scrape))

            if not new_urls:
                break
            else:
                urls_to_scrape = urls_to_scrape + new_urls

                print("Found {} new articles after {} iterations for {}.".format(
                    len(urls_to_scrape),
                    iteration,
                    search_tag)
                )

            iteration += 1

    print("Found {} new articles in total. Start scraping...".format(len(urls_to_scrape)))

    return urls_to_scrape
