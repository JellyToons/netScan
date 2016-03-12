# Author: Sai Uday Shankar
# Email: skorlimarla@unomaha.edu

from pymongo import MongoClient
from datetime import date
import shutil
import os
import sys
import re


# Pop goes the database
# casual reference to
# James Patterson's pop goes the weasel
# Do read that book, not this code!
'''
mongo_location:
    Picks mongo URL dynamically from current user's home
    directory. It is expected that the user has
    a directory .netscan with a file netScan.conf.
    Also it is expected that netScan.conf has mongo db url
'''
def mongo_location():
    mongo_url = ''
    with open(os.path.expanduser("~/"+'/.netScan/netScan.conf')) as conf:
        for line in conf:
            if 'mongo_url' in line:
                mongo_url= line.split(" ")[1]
            else:
                mongo_url = 'mongodb://localhost:27017/'
    return mongo_url

# client that will talk to the database
client = MongoClient(mongo_location())

# netScanDB Database for netScan
cpe_db = client['netScanDB']

# The above mongoDB will have it's first cpe_collection
# CPEs from NVD - Let's call it cpe_collection
cpe_collection = cpe_db.cpe_collection

# Method for dropping CPE collection
'''
drop_collection:
    Method for dropping collections
    pass collection name to be dropped
    Ex: drop_collection(cpe_collection)
'''
def drop_cpe_collection():
    cpe_collection.drop()
    if get_cpes_count() == 0:
        print("[+] {} dropped".format(cpe_collection))

# Generic method for inserting elements into a colleciton
# use bulk inserts for inserting many things at once
'''
db_insert(cpe_collection, "cpe:/a:apache:http_server:2.2.0")
    pass a collections name and what is to be posted into
    the collection
'''

def db_insert(post):
    preq = cpe_collection.find_one(post)
    post = post
    if preq is None:
        post_id = cpe_collection.insert_one(post).inserted_id
        return post_id
    else:
        print("[-] Existing record")
        print(preq)
        return None

def db_insert_bulk(multi_posts):
    multi_posts = multi_posts
    post_ids = cpe_collection.insert_many(multi_posts)
    # Huge list will be retured
    # If lot of posts are inserted into
    # the database
    return post_ids.inserted_ids

# Count items in a collection
'''
get_cpes_count
    posts in cpe_collection
'''
def get_cpes_count():
    return cpe_collection.count()
