from splinter import Browser
from bs4 import BeautifulSoup as soup
import pandas as pd
import datetime as dt

def scrape_all():

    # Initiate headless driver for deployment
    browser = Browser('chrome', executable_path="chromedriver", headless=True)

    news_title, news_paragraph = mars_news(browser)

    # Run all scraping functions and store results in a dictionary
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": featured_image(browser),
        "facts": mars_facts(),
        "mars_weather": mars_weather(browser),
        "hemisphere_images": hemi_img_titles(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()   
    return data

def mars_news(browser):

    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    try:
        slide_elem = news_soup.select_one('ul.item_list li.slide')

        slide_elem.find("div", class_='content_title')

        # Use the parent element to find the first a tag and save it as `news_title`
        news_title = slide_elem.find("div", class_='content_title').get_text()
        #news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
        # news_p

    except AttributeError:
        return None, None

    return news_title, news_p

def featured_image(browser):
    # Visit URL
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Find and click the full image button
    full_image_elem = browser.find_by_id('full_image')
    full_image_elem.click()

    # Find the more info button and click that
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_elem = browser.links.find_by_partial_text('more info')
    more_info_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    try:
        # find the relative image url
        img_url_rel = img_soup.select_one('figure.lede a img').get("src")
        # img_url_rel

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    img_url = f'https://www.jpl.nasa.gov{img_url_rel}'
    # img_url

    return img_url


def mars_facts():
    
    try:
        # ### Mars Facts
        df = pd.read_html('http://space-facts.com/mars/')[0]
        # df.head()

        df.columns=['Description', 'Mars']
        df.set_index('Description', inplace=True)
        # df

    except AttributeError:
        return None

    return df.to_html(classes="table tables-striped")

def mars_weather(browser):

    # Visit the weather website
    url = 'https://mars.nasa.gov/insight/weather/'
    browser.visit(url)

    # Parse the data
    html = browser.html
    weather_soup = soup(html, 'html.parser')

    try:
        # Scrape the Daily Weather Report table
        weather_table = weather_soup.find('table', class_='mb_table')
        # print(weather_table.prettify())

    except AttributeError:
        return None

    return (weather_table.prettify())


def hemi_img_titles(browser):
    
    # # D1: Scrape High-Resolution Mars’ Hemisphere Images and Titles
    # 1. Use browser to visit the URL 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    html_main_pg = browser.html
    hemi_soup1 = soup(html_main_pg, 'html.parser')

    # 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

    # 3. Write code to retrieve the image urls and titles for each hemisphere.
    # creating a list to hold titles
    hemi_titles = []

    # getting all 4 titles for all 4 hemispheres
    hemi_orig_titles = hemi_soup1.find_all('h3')
    print(hemi_orig_titles)

    try:
        # 3. Write code to retrieve the image urls and titles for each hemisphere.
        for title_each in hemi_orig_titles:
            
            #creating empty dictionary for img_url and title
            hemi_dict = {}
    
            # Getting titles for 4 hemispheres
            title_text = title_each.get_text()
            #print(title_text)
            title_split_value = title_text.split('Enhanced')
            title = title_split_value[0]
            #print(title)
            # getting url_end to visit new browser (final_browser)
            url_end = title_text.split()[0]
            #print(end_url)
        
            # Getting image url
            url_start = 'https://astrogeology.usgs.gov'
            url_middle = '/search/map/Mars/Viking/'
            # url_end used from above setion
            final_url = f"{url_start}{url_middle}{url_end}"
            # print(final_url)
 
            # Getting image url
            browser.visit(final_url)
            html_img_pg = browser.html
            hemi_soup2 = soup(html_img_pg, 'html.parser')
            img_pg = hemi_soup2.find("div", class_='downloads')
            full_img_url = img_pg.a['href']
            # print(full_img_url)
    
            # Appending to dictionary 
            hemi_dict.update({'img_url': full_img_url, 'title': title})
            # print(hemi_dict)
    
            # appending dictionary to hemisphere_image_urls
            hemisphere_image_urls.append(hemi_dict)
            #print(hemisphere_image_urls)

            # 4. Print the list that holds the dictionary of each image url and title.
            # hemisphere_image_urls

            # 5. Quit the browser
            browser.quit()

    except AttributeError:
        return None
    
    return hemisphere_image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())