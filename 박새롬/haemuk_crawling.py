#!/usr/bin/env python
# coding: utf-8

# In[5]:


import requests
from bs4 import BeautifulSoup


# In[9]:


base_url = 'https://www.haemukja.com'
main_url = base_url + '/recipes'


# In[10]:


resp = requests.get(main_url, params={
    'page': 1
})


# In[11]:


soup = BeautifulSoup(resp.text)
recipe_list = soup.select('a.call_recipe.thmb')
recipe_list[0]


# In[12]:


url_list = []
for item in recipe_list:
    url_list.append(base_url+item.get('href'))


# In[13]:



url_list


# In[16]:


import tqdm


# In[ ]:


content_list = []


# In[17]:


content_list = []
for sample in tqdm.tqdm(url_list):
    resp = requests.get(sample)
    content_list.append(resp.text)


# In[18]:


content_list


# In[19]:


import time


# In[20]:


time.sleep(10)


# In[ ]:




