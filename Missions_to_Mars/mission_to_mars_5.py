#!/usr/bin/env python
# coding: utf-8

# # Mission to Mars: Homework on Scraping and Web Analysis: Alternative Approach

# ##Scrape https://mars.nasa.gov/news/ and collect News Titles and Paragraphs

# In[85]:


#Import dependencies. Will use pandas for processing, BeautifulSoup to grab data, requests to pull html text, and MongoDB
#and Splinter for repository data storage.
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser


# In[86]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[87]:


print("scraping started")


# # 1. Mars News Articles

# ### URL for collecting html data on Mars

# In[88]:


url = "https://mars.nasa.gov/news"


# ### Browser.visit to view URL 

# In[89]:


browser.visit(url)


# ### Alternative approach: Grab data from 'li' tags as a list, then iterate to extract title, paragraph text, and reference for making a list of dictionaries suitable for MongoDB.

# In[90]:


#Alternative try to grab <li> tags, which have all of the articles.
#Then use iteration for loop to extract the title, teaser paragraph, and reference.
#Empty list for appending dictionaries of data for articles.
top_data = []

#Iteration knowing 40 articles per page and target of 400 articles
#for x in range(1,11):
    
html = browser.html
soup = bs(html, 'html.parser')

init_data = soup.find_all('li', class_='slide')

#Construct a list of dictionaries with these data for incorporation into MongoDB. Include
#'mars.nasa.gov' to enable direct use of the reference as a URL.
for item in init_data:
    title = item.find('div', class_='content_title').text
    teaser = item.find('div', class_='rollover_description_inner').text
    ref = 'mars.nasa.gov' + item.a['href']
    
    dictionary = {
        'section': 'news',
        'title': title,
        'teaser': teaser,
        'reference': ref  
    }
    
    top_data.append(dictionary)


# ### Check top_data list of dictionaries to confirm formatting and data

# In[91]:


len(top_data)


# In[92]:


#top_data[0]


# In[93]:


#top_data[39]


# # 2. JPL Mars Space Images

# ### Url for Mars Image

# In[94]:


url_2 = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'


# ### Visit url with browser, then create BeautifulSoup object to grab image information.

# In[95]:


browser.visit(url_2)


# In[96]:


html_2 = browser.html
soup_2 = bs(html_2, 'html.parser')


# In[97]:


raw_image_data = soup_2.find_all('article', class_="carousel_item")
#raw_image_data


# ### raw_image_data is a list, so take element [0] to extract string data on the 'style' tag. Extract the reference url for the full-size image and add the full information for generating the complete url. 

# In[98]:


# Little tricky because only one element in list. j element ([0]) and isolate
# the 'style' tag. The url is not a tag, so can't use it to isolate the url information.
for j in raw_image_data:
    raw_url = j['style']


# In[99]:


featured_image_url = 'https://www.jpl.nasa.gov' + raw_url.split("'")[1]


# In[100]:


featured_image_url


# ### Create dictionary for featured image.

# In[101]:


featured_image_dict = {
    #'section': 'featured_image',
    'featured_image_url': featured_image_url
}
featured_image_dict


# # 3. Mars Weather

# ### The url for Mars weather via twitter.com.

# In[102]:


url_3 = 'https://twitter.com/marswxreport?lang=en'


# In[103]:


browser.visit(url_3)


# ### Setup browser.html and create BeautifulSoup object for parsing.

# In[104]:


html_3 = browser.html
soup_3 = bs(html_3, 'html.parser')


# ### In other cases, used find_all to get all instances. I think this time we want the most recent weather data, so used .find. 

# In[105]:


mars_weather_raw = soup_3.find('div', class_="js-tweet-text-container")
mars_weather_raw


# ### Find nice image url for the Sol weather data. Twitter kept "twitting out" on me. Found a NASA website with data from the insight lander. 'https://mars.nasa.gov/layout/embed/image/insightweather/'

# ### Extract current Mars weather from the twitter url current data.

# In[106]:


current_mars_weather = mars_weather_raw.p.text.replace('\n', ', ').split('pic')[0]
current_mars_weather


# ### Create dictionary for these weather data.

# In[107]:


mars_weather_dict = {
    'section': 'weather',
    'current_mars_weather': current_mars_weather
}
#mars_weather_dict


# # 4. Mars Facts 

# ### New url for Mars Facts Website 

# In[108]:


url_4 = 'https://space-facts.com/mars/'


# ### Use Pandas to extract table information and reference for inclusion in website.

# In[109]:


tables = pd.read_html(url_4)


# In[110]:


len(tables)


# In[111]:


# Tables[0] and [1] have relevant data for use.


# In[112]:


mars_data = tables[0]


# In[113]:


mars_comparison_data = tables[1]


# In[114]:


# Rename columns and set index to Parameters


# In[115]:


renamed_mars_data = mars_data.rename(columns = {0: 'Parameters', 1: 'Measurements'})
#renamed_mars_data


# In[116]:


#mars_comparison_data


# ### Export dataframes as html formatted tables.

# In[117]:


renamed_mars_data.to_html('Mars_Data_Table.html')


# In[118]:


mars_comparison_data.to_html('Mars_Earth_Comparison_Data.html')


# ### Create list of dictionaries for mars data

# In[119]:


mars_data = [
    {
    'section': 'data_table',
    'data_table_1': 'Mars_Data.html'
    },
    {
    'section': 'data_table',
    'data_table_2': 'Mars_Earth_Comparison_Data.html'   
    }
]
#mars_data


# # 5. Mars Hemispheres

# ### URLs for high resolution images of Martian hemispheres. Attepmted to find a single webpage with all of these links, but did not find one. Will have to scrape each individual webpage, one for each Martian hemisphere. Main URL for website below.

# In[120]:


#url_5 = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'


# ### Cerberus Hemisphere Enhanced

# In[121]:


url_5a = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced'


# In[122]:


browser.visit(url_5a)


# In[123]:


html_5a = browser.html
soup_5a = bs(html_5a, 'html.parser')


# In[124]:


cerberus_raw = soup_5a.find_all('img', class_="wide-image")


# In[125]:


for data in cerberus_raw:
    cerberus_url = 'https://astrogeology.usgs.gov' + data['src']


# In[126]:


cerberus_url


# ### Schiaparelli Hemisphere Enhanced

# In[127]:


url_5b = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced'


# In[128]:


browser.visit(url_5b)


# In[129]:


html_5b = browser.html
soup_5b = bs(html_5b, 'html.parser')


# In[130]:


schiaparelli_raw = soup_5b.find_all('img', class_="wide-image")


# In[131]:


for data in schiaparelli_raw:
    schiaparelli_url = 'https://astrogeology.usgs.gov' + data['src']


# In[132]:


schiaparelli_url


# ### Syrtis Major Hemisphere Enhanced 

# In[133]:


url_5c = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced'


# In[134]:


browser.visit(url_5c)


# In[135]:


html_5c = browser.html
soup_5c = bs(html_5c, 'html.parser')


# In[136]:


syrtis_major_raw = soup_5c.find_all('img', class_="wide-image")


# In[137]:


for data in syrtis_major_raw:
    syrtis_major_url = 'https://astrogeology.usgs.gov' + data['src']


# In[138]:


syrtis_major_url


# ### Valles Marineris Hemisphere Enhanced

# In[139]:


url_5d = 'https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced'


# In[140]:


browser.visit(url_5d)


# In[141]:


html_5d = browser.html
soup_5d = bs(html_5d, 'html.parser')


# In[142]:


valles_marineris_raw = soup_5d.find_all('img', class_="wide-image")


# In[143]:


for data in valles_marineris_raw:
    valles_marineris_url = 'https://astrogeology.usgs.gov' + data['src']


# In[144]:


valles_marineris_url


# ## Construct image titles and url's list of dictionaries

# In[145]:


titles = ['Cerberus Hemisphere Enhanced', 'Schiaparelli Hemisphere Enhanced', 'Syrtis Major Hemisphere Enhanced', 'Valles Marineris Hemisphere Enhanced']
urls = [cerberus_url, schiaparelli_url, syrtis_major_url, valles_marineris_url]

image_urls= []

for x in range(len(titles)):
    dictionary = {
    'section': 'hemispheres',
    'hemisphere': titles[x],
    'image_url': urls[x]    
    }
    
    image_urls.append(dictionary)


# In[146]:


image_urls


# # 6. Combine all Dictionaries and Lists of Dictionaries into a single list of dictionaries: total_mars_data.

# ### First construct a list to total_mars_data, then iterate through all other lists and dictionaries and append.

# In[152]:


total_mars_data = []


# In[153]:


# top_data is a list of dictionaries with recent articles. Iterate through list and append dictionaries to total_mars_data list.
for d in top_data:
    total_mars_data.append(d)


# In[154]:


# next append featured_image_url dictionary
total_mars_data.append(featured_image_dict)


# In[155]:


# next append mars_weather_dict
total_mars_data.append(mars_weather_dict)


# In[156]:


# next append mars data table information by iteration as in top_data.
for m in mars_data:
    total_mars_data.append(m)


# In[157]:


# same approach as for top_data list.
for u in image_urls:
    total_mars_data.append(u)


# In[158]:


#total_mars_data


# In[159]:


len(total_mars_data)


# # 7. Transfer the total_mars_data into a Mongo Database called Mars_DataDB

# ### Initialize pymongo connection to mongod on local machine port localhost:27017(make certain mongod is running)

# In[160]:


conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)


# ### Define database (Mars_DataDB) and collection (db.scraped_mars_data)

# In[161]:


db = client.Mars_DataDB
collection = db.scraped_mars_data


# ### Drop the data in collection before appending new data.

# In[162]:


collection.drop()


# ### Loop through total_mars_data and insert each dictionary into the scraped_mars_data collection. Note that a try/except error catching may be needed if some of the scraping data is not formatted correctly.

# In[163]:


#try: (remember that for loop will need to be indented if try is used)
for data in total_mars_data:
    collection.insert_one(data)
    
#except (remember to enter the exception if try fails)


# ### Checked MongoDB and confirmed Mars_DataDB and the scraped_mars_data collection were created and active. All data was inserted.

# In[164]:


print("scraping finished")


# In[165]:


total_mars_data


# In[166]:


total_mars_data[40]


# In[ ]:




