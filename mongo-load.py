import facebook, os
from pymongo import *

api = os.environ.get('FB_API')
uri = os.environ.get('FROM_EMAIL')
client = MongoClient(uri)
db = client.facebook
coll = db.free_and_for_sale

# Get max updated_time to load incrementally
last_update = coll.find_one(sort=[('updated_time', -1)])['updated_time']
graph = facebook.GraphAPI(access_token=api)
# 385662371445806 - UW Free & For Sale Group ID
fbdata = graph.get_object(id='385662371445806/feed', since=last_update, date_format='U')['data']
if fbdata:
    ins_id = coll.insert(fbdata)
client.close()
