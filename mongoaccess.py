
# coding: utf-8

# In[2]:


import pprint
import pymongo


# In[9]:


def main():

    # 1. Connect to MongoDB instance running on localhost
    # client = pymongo.MongoClient()
    # client = pymongo.MongoClient('localhost',27017)
    # client = pymongo.MongoClient('mongodb://localhost:27017/')
    client = pymongo.MongoClient('mongodb://192.168.56.110:27017/')
    
    # Access the 'restaurants' collection in the 'test' database
    collection = client.test.restaurants

    # 2. Insert 
    new_documents = [
        {"name":"Sun Bakery Trattoria", "stars":4, "categories":["Pizza","Pasta","Italian","Coffee","Sandwiches"]},
        {"name":"Blue Bagels Grill", "stars":3, "categories":["Bagels","Cookies","Sandwiches"]},
        {"name":"Hot Bakery Cafe","stars":4,"categories":["Bakery","Cafe","Coffee","Dessert"]},
        {"name":"XYZ Coffee Bar","stars":5,"categories":["Coffee","Cafe","Bakery","Chocolates"]},
        {"name":"456 Cookies Shop","stars":4,"categories":["Bakery","Cookies","Cake","Coffee"]}]

    collection.insert_many(new_documents)

    # 3. Query 
    for restaurant in collection.find():
        pprint.pprint(restaurant)

    # 4. Create Index 
    collection.create_index([('name', pymongo.ASCENDING)])

    # 5. Perform aggregation
    pipeline = [
        {"$match": {"categories": "Bakery"}},
        {"$group": {"_id": "$stars", "count": {"$sum": 1}}}]
    pprint.pprint(list(collection.aggregate(pipeline)))


# In[11]:


if __name__ == '__main__':
    main()

