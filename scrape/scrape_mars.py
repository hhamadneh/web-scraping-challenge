#!/usr/bin/env python
# coding: utf-8

# # Import dependencies

# In[1]:


from bs4 import BeautifulSoup as bs 
import os, json
import pandas as pd
import requests
from splinter import Browser
import splinter
import time

def init_chrome():
    executable_path = {'executable_path' : 'chromedriver.exe'}
    browser = splinter.Browser('chrome')
    return browser

# In[4]:

def mars_news():
    returned_list = []
    browser = init_chrome()
    baseurl = 'https://mars.nasa.gov/news/'
    browser.visit(baseurl)
    html = browser.html
    soup = bs(html, 'html.parser')
    LIs = soup.find_all('li', class_='slide')
    for i in range (0, len (LIs)):
        news_title = LIs[i].find("div", class_='content_title')
        news_text = LIs[i].find("div", class_='article_teaser_body')
        news_title_holder = news_title.text.strip()
        news_text_holder = news_text.text.strip()
        print("newsTitle = ",news_title_holder ,"\n")
        print ("newsText = ",news_text_holder ,"\n----------------------------------")
        returned_list.append ({'newsTitle': news_title_holder, 'newsText': news_text_holder})
    return returned_list
    browser.quit()

def JPL_images():
    browser = init_chrome()
    base_url = 'https://www.jpl.nasa.gov'
    JPL_URL = base_url + '/spaceimages/?search=&category=Mars'
    browser.visit(JPL_URL)
    html = browser.html
    soup = bs(html, 'html.parser')
    medium_image_url=soup.find("a", class_ = "button fancybox")["data-fancybox-href"]
    featured_image_med = base_url + medium_image_url

    featured_image = soup.find("article", class_='carousel_item')['style']
    wallpaper_size = featured_image.split("'")[1].split("'")[0]
    featured_image_wall = base_url + wallpaper_size

    browser.find_by_id("full_image").click()
    browser.find_by_text("more info     ").click()
    html = browser.html
    soup = bs(html, 'html.parser')
    featured_img = soup.find("img", class_='main_image')['src']
    featured_img_full = base_url + featured_img
    return featured_img_full
    browser.quit()

def Mars_Facts():
    returned_facts_list = []
    browser = init_chrome()
    mars_fact_url = 'https://space-facts.com/mars/'
    browser.visit(mars_fact_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    news_titles = soup.find("table", class_='tablepress tablepress-id-p-mars')
    #for i in range (len(news_titles)):
    print(news_titles)
    mars_facts = pd.read_html (mars_fact_url)
    rights = list (mars_facts[0][0])
    lefts = list (mars_facts[0][1])
    facts_df = pd.DataFrame ({'Name': rights,
                            'values' : lefts})
    for i in range (len (rights)):
        returned_facts_list.append ({rights[i].strip(":"): lefts [i]})
    return returned_facts_list
    browser.quit()

def Mars_Hemispheres():
    browser = init_chrome()
    base_USGS_URL = 'https://astrogeology.usgs.gov/'
    USGS_Astrogeology_url = base_USGS_URL + 'search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(USGS_Astrogeology_url)
    html = browser.html
    soup = bs(html, 'html.parser')
    visit_list = []
    clicks = soup.find_all('a', class_='itemLink product-item')
    for i in clicks:
        #print (i.str.split('href=')[1])
        temp_str = base_USGS_URL + str (i).split ('href=')[1].split('>')[0].strip ('"')
        temp_str = temp_str.replace("//","/")
        if temp_str not in visit_list:
            visit_list.append (temp_str)
    print (visit_list)

    img_url_list = []
    title_list = []
    i = 0
    for i in range (len (visit_list)):
        browser.visit(visit_list [i])
        html = browser.html
        soup = bs(html, 'html.parser')
        title = soup.find_all('h2', class_='title')
        img_url = soup.find_all('a')[4]
        title_list.append (str(title).split('>')[1].split('<')[0])
        img_url_list.append (str(img_url).split('"')[1])
    print (title_list)
    print (img_url_list)

    hemisphere_image_urls = []
    for i in range (len (img_url_list)):
        hemisphere_image_urls.append ({'title': title_list[i], 'img_url': img_url_list [i]})
        print (hemisphere_image_urls[i]['title'])
        print (hemisphere_image_urls[i]['img_url'] + '\n')
    return hemisphere_image_urls
    browser.quit()

#print (mars_news())