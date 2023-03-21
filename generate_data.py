
from faker import Faker
import pandas as pd
from faker_food import FoodProvider
import random

fake = Faker('es_ES')
fake.add_provider(FoodProvider)


def random_openinghour():
    return str(fake.random_int(8,10))+":00-"+str(fake.random_int(18,22))+":00"

def random_address():
    return fake.street_name()+ ", " + fake.building_number() +", "+fake.city()


def generate_product_data(out_file, number_of_records):

    product_list = []
    columns_list = ['id', 'brand', 'type_product', 'calories', 'satured_fat_percentage', 'sugar_percentage']
    for val in range(number_of_records):
        product_list.append([fake.unique.random_int(1,number_of_records*5), fake.unique.fruit(),  'fruit', fake.random_int(10,400),
                           round(random.uniform(0.0, 20.0),2), round(random.uniform(0.0, 40.0),2)])

    df = pd.DataFrame(product_list, columns=columns_list)
    df.to_csv(out_file, mode='w', index = False)

    return product_list


def generate_store_data(out_file, number_of_records):

    store_list = []
    columns_list = ['id','name','address','opening_hours']
    for val in range(number_of_records):
        store_list.append([fake.unique.random_int(1,number_of_records*5),str(fake.unique.company()), random_address(), random_openinghour()])

    df = pd.DataFrame(store_list, columns=columns_list)
    df.to_csv(out_file, mode='w', index=False)

    return store_list


def generate_association_data(out_file, number_of_records, stores, products):

    association_list = []
    columns_list = ['store_id','product_id', 'price'  ]
    for val in range(number_of_records):
        random_store = random.choice(stores)
        random_product = random.choice(products)
        association_list.append([random_store[0], random_product[0], round(random.uniform(0.5, 10.0), 2) ])

    df = pd.DataFrame(association_list, columns=columns_list)
    df.to_csv(out_file, mode='w', index=False)

    return association_list




stores = generate_store_data(out_file= 'csvs/store_data.csv', number_of_records=20)
products = generate_product_data(out_file= 'csvs/product_data.csv', number_of_records=20)
associations = generate_association_data(out_file= 'csvs/association_data.csv', number_of_records=20,
                                         stores=stores, products=products )