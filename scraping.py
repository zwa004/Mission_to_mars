# Import Splinter and BeautifulSoup
from splinter import Browser
from bs4 import BeautifulSoup as soup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import datetime as dt

def hemisphere_scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://marshemispheres.com/'

    browser.visit(url)
    # 1. Use browser to visit the URL 

# 2. Create a list to hold the images and titles.
    hemisphere_image_urls = []

# 3. Write code to retrieve the image urls and titles for each hemisphere.
    html = browser.html
    img_soup = soup(html, 'html.parser')
    img_soup
    # Link of each hemisphere page
    browser_links = browser.find_by_css('a.product-item img')
    # Loop through each image based on the number of product-item's there are ie range len
    for img in range(len(browser_links)):
        # Dict for img and titles
        img_and_titles = {}
        
        # Dynamic clicking for each index in the list of browser links
        browser.find_by_css('a.product-item img')[img].click()    
        
        # Add url to dict 
        img_and_titles['url'] = browser.find_by_text('Sample')['href']
        
        # Add title 
        img_and_titles['title'] = browser.find_by_css('h2.title').text
        
        
        #print(img_and_titles)
        hemisphere_image_urls.append(img_and_titles)
        browser.back()
        
    # 4. Print the list that holds the dictionary of each image url and title.
    print(hemisphere_image_urls)
    # 5. Quit the browser
    browser.quit()
    return hemisphere_image_urls
def scrape_all():
    # Initiate headless driver for deployment
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    news_title, news_paragraph = mars_news(browser)
    
    # Run all scraping functions and store results in dictionary
    data = {
      "news_title": news_title,
      "news_paragraph": news_paragraph,
      "featured_image": featured_image(browser),
      "facts": mars_facts(),
      "hemisphere_images": hemisphere_scrape(),
      "last_modified": dt.datetime.now()}
    
    browser.quit()
    return data

def mars_news(browser):
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com'
    browser.visit(url)

    # Optional delay for loading the page
    browser.is_element_present_by_css('div.list_text', wait_time=1)

    #Convert the browser html to a soup object the quit the browser
    html = browser.html
    news_soup = soup(html, 'html.parser')

    # Add error handling
    try:
        slide_elem = news_soup.select_one('div.list_text')
        slide_elem.find('div', class_='content_title')

        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        news_title = slide_elem.find('div', class_='content_title').get_text()
        news_title

        # Use the parent element to find the paragraph text
        news_p = slide_elem.find('div', class_='article_teaser_body').get_text()
        news_p
    except AttributeError:
        return None, None
    
    return news_title, news_p

# ### Featured Images
# 

def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)


    # Find and click the full image button
    full_image_elem = browser.find_by_tag('button')[1]
    full_image_elem.click()

    # Parse the resulting html with soup
    html = browser.html
    img_soup = soup(html, 'html.parser')

    # Add error handling
    try:
        # Find the relative image url
        img_url_rel = img_soup.find('img', class_='fancybox-image').get('src')
        img_url_rel
        
    except AttributeError:
        return None

    # Use the base URL to greate an absolute URL
    img_url = f'https://spaceimages-mars.com/{img_url_rel}'
    return img_url

def mars_facts():   
    # Add error handling
    try:
        # Use 'read_htlm' to scrape the facts table into a dataframe
        df = pd.read_html('https://galaxyfacts-mars.com')[0]
    
    except BaseException:
        return None
    
    # Assigne columns and set index of dataframe
    df.columns=['description', 'Mars', 'Earth']
    df.set_index('description', inplace=True)

    # Convert dataframe into HTML, add bootstrap
    return df.to_html()

if __name__ == "__main__":
    
    # If running as script, print scraped data
    print(scrape_all())








