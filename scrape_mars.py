from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape_info():
    # Set up Splinter
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    # Visit replanetscience.com
    url1 = "https://redplanetscience.com/"
    browser.visit(url1)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the latest News Title #news > div:nth-child(1) > div > div.col-md-8 > div > div.content_title
    news_title = soup.find('div', class_='content_title').text
    print(news_title)

    # Get the paragaph text for #news > div:nth-child(1) > div > div.col-md-8 > div > div.article_teaser_body
    news_p = soup.find('div', class_='article_teaser_body').text
    print(news_p)

    # Set up Splinter
    # executable_path = {'executable_path': ChromeDriverManager().install()}
    # browser = Browser('chrome', **executable_path, headless=False)

    # Visit spaceimages-mars.com
    url2 = "https://spaceimages-mars.com/"
    browser.visit(url2)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    sopa = bs(html, "html.parser")

    # Find the source for the featured image body > div.header > div > a https://spaceimages-mars.com/image/featured/mars2.jpg
    relative_image_path = sopa.find(
        'a', class_='showimg fancybox-thumbs')['href']
    featured_image_url = url2 + relative_image_path
    print(featured_image_url)

    # Get table facts from galaxyfacts-mars.com using pandas
    mars_table = pd.read_html('https://galaxyfacts-mars.com/')
    df = mars_table[1]
    html_table = df.to_html()

    # Get hemisphere images
    hemispheres = ['Cerberus', 'Schiaparelli', 'Syrtis', 'Valles']

    hemisphere_image_urls = []
    dic = {}

    for hemisphere in hemispheres:

        # Get hemisphere images
        url3 = "https://marshemispheres.com/"
        browser.visit(url3)

        # Click on the next page
        browser.click_link_by_partial_text(hemisphere)

        time.sleep(1)

        # Scrape page into Soup
        html = browser.html
        sop = bs(html, "html.parser")

        # Get the title and urls
        img_url = url3 + sop.find_all('a', target="_blank")[2]['href']
        title = sop.find_all('h2', class_='title')[0].text
        dic = {"title": title, "img_url": img_url}
        hemisphere_image_urls.append(dic)

    hemisphere_image_urls

    # Store mars data
    mars_data = {"news": news_title, "news_p": news_p,
                 "img_fea": featured_image_url, "table": html_table, "hemis_pic": hemisphere_image_urls}

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
