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

# This code will create a list of all of the recommendations for
# all of the searched movies.  Note that some of the data in the db is
# bad.  For example, rec_list[9203] is a bad data type.
# So I have to put in code to make sure that the data is a string before
# putting it into the list.


rec_list = []
recs = db.items.find({},{"_id":0, "recommended":1});
for rec in recs:
    if (len(list(rec.values()))!= 0):
        for opt in list(rec.values())[0]:
            if isinstance(opt, str):
                rec_list.append(opt)

# And here we tally the recommendations.
# Alternatively, we could have used the 'count' function as
# [[x,rec_list.count(x)] for x in set(rec_list)]

rec_dict = dict(Counter(rec_list))
rec_df = pd.DataFrame.from_dict(rec_dict, orient='index')
rds = rec_df.sort_values(by=0, ascending=False)
rds.reset_index(inplace=True)
rds.rename(columns={'index':'recommendation', 0:'count'}, inplace=True)

# And finally we print.
# These are the most recommended movies.  They can serve as good recs for
# people looking for a generic movie to watch.

rds_short = rds[0:30]
fig = px.bar(rds_short, x="recommendation", y="count")
fig.show()

