import django
import os
import csv
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
django.setup()


from home.models import *

#python manage.py dbshell
#drop table 이름
#delete from django_migrations where app = 'home'

# ##########일반적인 방법
# CSV_PATH = 'C:/Users/user/Desktop/밀화부리/mysite/ko.csv' 

# with open(CSV_PATH, newline='',encoding='UTF-8') as csvfile: 
#     data_reader = csv.DictReader(csvfile) 
#     for row in data_reader: 
#         print(row) 
#         home.objects.create( name = row['name'], ingredients = row['ingredients'], ingredients_pre = row['ingredients_pre'],url = row['url'], serving = row['serving'], cnt = row['cnt'],cluster = row['cluster'] )



# ####벌크업데이트

# CSV_PATH = 'C:/Users/user/Desktop/project_cooking/Website/final_recipe_df.csv' 

# with open(CSV_PATH, newline='',encoding='UTF-8') as csvfile: 
#     data_reader = csv.DictReader(csvfile) 
 
#     bulk_list = []
#     for row in data_reader:
#         bulk_list.append(Home(
#                 name=row['name'],
#                 ingredients=row['ingredients'],
#                 ingredients_pre=row['ingredients_pre'],
#                 url=row['url'],
#                 serving=row['serving'],
#                 cnt=row['cnt'],
#                 cluster=row['cluster'],
#                 ))
#     Home.objects.bulk_create(bulk_list)







# for i in range(1,19):
#     row = Home.objects.get(pk=i)
#     row.delete()





