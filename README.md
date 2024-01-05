## Scripts purpose

**getItems** is to download the saved items from the marketplace of Facebook.  
**getGroups** is to download the groups I am part of on Facebook.  
**get_posts_from_groups.py** is to download the posts from the groups I am part of on Facebook, this script generates three files:  
- Posts.csv
- commerce_ids.csv
- rejected.txt


**download_commerce_ids_data.py** is to download the data of the commerce ids that get_posts_from_groups.py generated. This generates the file Rentas_commerce_ids.csv and it can be loaded into QGIS.  
**download_items_data.py** is to download the data of the items that getItems generated. This generates the file Rentas_items.csv and it can be loaded into QGIS.  

## Execution order

**getGroups** -> **get_posts_from_groups.py** -> **download_commerce_ids_data.py**  
**getItems** -> **download_items_data.py**
