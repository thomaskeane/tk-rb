# Packages

import pymongo
import pandas as pd
from collections import Counter
import plotly.express as px

from config import utelly_api_key, mode, usecache
from config import mongoConn, mongoConnProd, mySQLConn
from config import remote_db_endpoint, remote_db_port, remote_db_user, remote_db_pwd, remote_db_name

IS_HEROKU = 'True'

# Connect to the database 'shows_db' and then grab the document collection, which is called 'items'
client = pymongo.MongoClient(mongoConn)
db = client.shows_db
items = db.items.find()

# This code grabs all of the services for all of the requested movies, and makes a bar
# graph to see which services have the largest library of the searched for movies.
# This information can be used by a customer who wants to know which service is the single
# most robust for having movies that the customer would want to see.

# Create a list to hold all of the services listed for all of the movies searched
# So if 200 movies are searched, and netflix has 150 of them, 'netflix' will appear in the list
# 150 times.  This list will be used to tally the movie availability count.

service_list = []

# Now grab all of the services that stream the movies the customers
# searched for, and put them in the service list

services = db.items.find({},{"_id":0, "services":1});
for service in services:
    if (len(list(service.values())) != 0):
        for opt in list(service.values())[0]:
            service_list.append(opt)
        
# Now use the counter function to tally the number of times each streaming service
# is mentioned.  Drop the tally into a data frame and then sort by frequency in descending order

service_dict = dict(Counter(service_list))
service_df = pd.DataFrame.from_dict(service_dict, orient='index')
sds = service_df.sort_values(by=0, ascending=False)
sds.reset_index(inplace=True)
sds.rename(columns={'index':'service preferred by user', 0:'count'}, inplace=True)

# Now plot the top 30 services, so that users can see which ones
# have the biggest library of shows of interest

sds_short = sds[0:30]
fig = px.bar(sds_short, x="service preferred by user", y="count")
fig.show()

