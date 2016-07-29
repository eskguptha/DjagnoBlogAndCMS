import sys
import os
import json
import MySQLdb
import MySQLdb.cursors
import csv
from urlparse import parse_qs, urlparse
db = MySQLdb.connect(host= "localhost",user="root",passwd="mysql",db="demo",cursorclass=MySQLdb.cursors.DictCursor)

cursor = db.cursor()

def get_data():
	json_data = {}
	category_data = []
	post_data = []
	
	# Category
	with open('aci.json') as data_file:
		json_data = json.load(data_file)
	for p,each_dict in enumerate(json_data):
		
		post_id = p+1
		image_url =  parse_qs(urlparse(each_dict['image_url']).query, keep_blank_values=True)
		category = each_dict['link'].split('/')[3]
		slug = "http://127.0.0.1/post/%s"%post_id
		each_dict.update({"url":slug, "image":image_url['n'][-1],"id":post_id,"categories":category,"vendor":"Autocar India","sku":post_id})
		del each_dict['image_url']
		del each_dict['link']
		post_data.append(each_dict)
		if category not in category_data:
			category_data.append(str(category))
	return post_data, category_data

def blog_insert():
	post_data, category_data = get_data()
	category_post_data = []
	category_data = tuple((i+1,each,'') for i, each in enumerate(category_data))


	query = "INSERT INTO blog_category VALUES (%s, %s,%s)"
	try:
		cursor.executemany(query, category_data)
		db.commit()
	except Exception as e:
		print e
		db.rollback()

	# Category Cache
	blog_category_cache = {}
	cursor.execute("SELECT * FROM blog_category ")
	blog_category_result = cursor.fetchall()
	for each in blog_category_result:
		blog_category_cache[each['name']] = each

	# Post
	post_values = tuple((each['post_id'], each['title'], 'auto Car', each['image_url'],'',each['link']) for j, each in enumerate(post_data))
	category_post_values = tuple((j+1, each['post_id'],  blog_category_cache.get(each['category'], '')['id']) for j, each in enumerate(post_data))
	query1 = "INSERT INTO blog_post VALUES (%s,%s,%s,%s, %s,%s)"
	query2 = "INSERT INTO blog_post_category VALUES (%s,%s,%s)"
	try:
		cursor.executemany(query1, post_values)
		cursor.executemany(query2, category_post_values)
		db.commit()
	except Exception as e:
		print e
		db.rollback()


	

	return True



def catalog_insert():
	json_data = {}
	category_data = []
	product_data = []
	category_post_data = []
	# Category
	csv_data = csv.DictReader(open('catalog.csv', 'rb'), delimiter=',')
	k =0
	for each_dict in csv_data:
		k = k+1
		category = each_dict['categories']
		category = json.loads(category)
		for item in category:
			if item not in category_data:
				category_data.append(str(item))
		each_dict['id'] = k
		product_data.append(each_dict)
	category_data = [(i+1,each,'') for i, each in enumerate(category_data)]
	query = "INSERT INTO catalog_category VALUES (%s, %s,%s)"
	try:
		#cursor.executemany(query, category_data)
		db.commit()
	except Exception as e:
		print e
		db.rollback()

	# Category Cache
	catalog_category_cache = {}
	cursor.execute("SELECT * FROM catalog_category ")
	catalog_category_result = cursor.fetchall()
	for each in catalog_category_result:
		each['id'] = int(each['id'])
		catalog_category_cache[each['name']] = each

	# Product
	product_values = [(each['id'], each['title'], each['sku'],each['vendor'],each['image'],float(each['price']),float(each['old-price']),'',each['url']) for each in product_data]
	print len(product_values)
	category_product_values = []
	j = 0 
	for each in product_data:
		category_list = json.loads(each['categories'])
		for item in category_list:
			j = j+1
			category_product_values.append((j+1,each['id'],catalog_category_cache[item]['id']))


	#category_product_values = [(j+1,j+1,  catalog_category_cache.get(each['categories'], '1')['id']) for j, each in enumerate(product_data)]

	query1 = "INSERT INTO catalog_product VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
	query2 = "INSERT INTO catalog_product_category VALUES (%s,%s,%s)"
	try:
		#cursor.executemany(query1, product_values)
		cursor.executemany(query2, category_product_values)
		db.commit()
	except Exception as e:
		print e
		db.rollback()
	return True




def blog_to_json():
	post_data, category_data = get_data()
	with open('autocar_catalog.json', 'w') as outfile:
	    json.dump(post_data, outfile,indent=4)
    	outfile.close()

if __name__=="__main__":
	blog_insert()
	catalog_insert()
	blog_to_json()
