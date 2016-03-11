import requests
import urllib2
import os
import json
from tabulate import tabulate

rest_name = []
rest_locality = []
rest_code = []
rest_avg_cost = []
rest_rating = []
query = raw_input("Enter the name of the location: ").split(' ')
initial_url = 'https://developers.zomato.com/api/v2.1/locations?query='
for i in range (0,len(query)):
	if(i==len(query)-1):
		initial_url = initial_url + query[i] + '&count=6&sort=rating'
	else:
		initial_url = initial_url + query[i] + '%20'

#print initial_url

api_key = '22b2050b2c779d35f5da049e8d414fcd'
url = 'https://developers.zomato.com/api/v2.1/locations?query=janakpuri&count=6'

#For location id and type extraction
data_location = {'Accept' : 'application/json', 'user-key' : '22b2050b2c779d35f5da049e8d414fcd', 'User-Agent' : 'curl/7.35.0'}
response = requests.get(initial_url, headers = data_location)
#print response.text
os.system('cls')

#To convert the response text(dictionary) to computer-readable script
location_stuff = response.json()


#To extract location_details like best rated restaurents, popularity, average cost for two, etc.
entity_id = location_stuff['location_suggestions'][0]['entity_id']
entity_type = location_stuff['location_suggestions'][0]['entity_type']


#For location details extraction
data_location_details = {'Accept' : 'application/json', 'user-key' : '22b2050b2c779d35f5da049e8d414fcd', 'User-Agent' : 'curl/7.35.0'}
url_ld = 'https://developers.zomato.com/api/v2.1/location_details?entity_id=%s&entity_type=subzone' % str(entity_id)
response = requests.get(url_ld, headers = data_location_details)
#print response.status_code
#print response.text
location_details_stuff = response.json()


#print location_details_stuff['best_rated_restaurant'][0]['restaurant']['name']
#print location_details_stuff['best_rated_restaurant'][0]['restaurant']['location']['address']



initial_search_url = 'https://developers.zomato.com/api/v2.1/search?q='
for i in range(0, len(query)):
	if(i == len(query)-1):
		initial_search_url = initial_search_url + query[i] + '&count=10&radius=5.2&sort=real_distance'
	else:
		initial_search_url = initial_search_url + query[i] + '%20'

#print initial_search_url


data_search = {'Accept' : 'application/json', 'user-key' : '22b2050b2c779d35f5da049e8d414fcd', 'User-Agent' : 'curl/7.35.0'}
response = requests.get(initial_search_url, headers = data_search)

#print response.text


resp_dict = json.loads(response.text)
for i in range(0,9):
	#print resp_dict['restaurants'][i]['restaurant']['name']
	rest_name.append(resp_dict['restaurants'][i]['restaurant']['name'])
	rest_locality.append(resp_dict['restaurants'][i]['restaurant']['location']['locality'])
	rest_code.append(resp_dict['restaurants'][i]['restaurant']['R']['res_id'])
	rest_avg_cost.append(resp_dict['restaurants'][i]['restaurant']['average_cost_for_two'])
	rest_rating.append(resp_dict['restaurants'][i]['restaurant']['user_rating']['aggregate_rating'])
#print rest_name
#print rest_locality
#print rest_code
#print rest_avg_cost

headers = ["Name","Locality","Code","Budget","Rating"]
#table = [[rest_name[0], rest_locality[0], rest_code[0], rest_avg_cost[0]]]
table = []

for i in range(0,9):
	table.insert(i,[rest_name[i],rest_locality[i],rest_code[i],rest_avg_cost[i], rest_rating[i]]) 
print tabulate(table, headers, tablefmt="rst", stralign='left')

