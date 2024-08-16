import os
from notion_client import Client

notion = Client(auth=open("token").read().strip())

from pprint import pprint
import json
d = notion.databases.query(database_id="1135332ccd614ae6bc7e962d3c4779d1")
for x in d["results"]:
   x = x["properties"]
   pprint({
     "start": x["Deadline"]["date"]["start"],
     "end": x["Deadline"]["date"]["end"],
     "status": x["Status"]["status"]["name"],
     "type": x["Type"]["select"]["name"],
     "subject": x["Subject"]["select"]["name"],
     "name": x["Name"]["title"][0]["plain_text"]
   })
   #pprint(x["properties"]["Name"]["title"][0]["plain_text"])
# https://www.notion.so/1135332ccd614ae6bc7e962d3c4779d1
