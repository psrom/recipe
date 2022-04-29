#!/usr/bin/env python
# coding: utf-8

# In[3]:


import json

with open('layer1.json', 'r') as f:
    json_data = json.load(f)


# In[5]:


json_data


# In[37]:


Ingredients = []
url = []
partition = []
title = []
Instructions = []


# In[38]:


# =============================================================
# 레시피 url, train/test 구분자, 레시피 제목, 레시피 재료, 레시피 순서
# 뽑아오기
# =============================================================

for i in range(len(json_data)):
    url.append(json_data[i]["url"])
    partition.append(json_data[i]["partition"])
    title.append(json_data[i]["title"])
    
    ingredients = []
    instructions = []
    for j in range(len(json_data[i]['ingredients'])):
        ingredients.extend(list(json_data[i]['ingredients'][j].values()))
    Ingredients.append(ingredients)
        
    
    for k in range(len(json_data[i]['instructions'])):
        instructions.extend(list(json_data[i]["instructions"][k].values()))
    Instructions.append(instructions)


# In[39]:


# 데이터 프레임 생성

import pandas as pd
df = pd.DataFrame({"Ingredients": Ingredients,
                  "URL": url,
                  "Partition": partition,
                  "Title": title,
                  "Instructions": Instructions})


# In[40]:


df


# In[41]:


df.to_csv('english_recipe.csv')


# In[44]:


# csv 확인 코드
# english = pd.read_csv('english_recipe.csv', index_col=0)
# english


# In[ ]:




