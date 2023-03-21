
import pandas as pd
import requests

url_post_store = "http://127.0.0.1:5001/store"
url_post_product = "http://127.0.0.1:5001/product"


print("\nCreating stores..")
df_store = pd.read_csv('csvs/store_data.csv')
num_created_stores = 0
for store in df_store.to_dict(orient='records'):
   post_response = requests.post(url_post_store, json=store)
   if(post_response.status_code != 200):
       print("Problem creating store " + str(store))
   else:
       num_created_stores += 1
print("\tStores created: " + str(num_created_stores))


print("\nCreating products..")
df_product = pd.read_csv('csvs/product_data.csv')
num_created_products = 0
for prod in df_product.to_dict(orient='records'):
    post_response = requests.post(url_post_product, json=prod)
    if (post_response.status_code != 200):
        print("Problem creating product " + str(prod))
    else:
        num_created_products += 1
print("\tProducts created: " + str(num_created_products))


print("\nCreating associations..")
df_association= pd.read_csv('csvs/association_data.csv')
num_assigned_prices = 0
for assoc in df_association.to_dict(orient='records'):
    url_assoc = url_post_product+"/"+str(assoc['product_id'])+"/price"
    post_response = requests.put(url_assoc, json=assoc)
    if (post_response.status_code != 200):
        print("Problem assigning price for " + str(assoc))
    else:
        num_assigned_prices += 1
print("\tPrices assigned: " + str(num_assigned_prices))


