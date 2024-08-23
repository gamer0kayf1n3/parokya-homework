import os
import datetime
from notion_client import Client
class Worklist:
    def __init__(self):
        self.notion = Client(auth=open("token").read().strip())
    def fetch(self):
        data = self.notion.databases.query(database_id="1135332ccd614ae6bc7e962d3c4779d1")
        properties = [x["properties"] for x in data["results"]]
        simplified_datalist = []
        for x in properties:

            temp = {
                "start": x["Deadline"]["date"]["start"],
                "end": x["Deadline"]["date"]["end"],
                "status": x["Status"]["status"]["name"],
                "type": x["Type"]["select"]["name"],
                "subject": x["Subject"]["select"]["name"],
                "name": x["Name"]["title"][0]["plain_text"]
            }
            if not include(temp["start"], temp["end"]): continue
            temp["start"] = dateparser(temp["start"])
            temp["end"] = dateparser(temp["end"])

            simplified_datalist.append(temp)
        return simplified_datalist

class TodayActivities:
    def __init__(self):
        self.notion = Client(auth=open("token").read().strip())
    def fetch(self):
        data = self.notion.databases.query(database_id="d2cf192ae4204ee9958a4c579295a3df")
        properties = [x["properties"] for x in data["results"]]
        def sortKey(x): 
            print(x)
            return x["Name"]['title'][0]['plain_text']
        properties.sort(key=sortKey)
        simplified_datalist = []
        for x in properties:
            temp = {
                "name": x["Name"]["title"][0]["plain_text"],
                "tags": [item["name"] for item in x["Tags"]["multi_select"]],
                "remarks": x['Remarks']['rich_text'][0]['plain_text'] if x['Remarks']['rich_text'] else ""
            }
            print(x)
            simplified_datalist.append(temp)
        return simplified_datalist



def dateparser(datestring):
    if datestring == None: return None
    date = datetime.datetime.fromisoformat(datestring)
    if date.hour == 0 and date.minute == 0 and date.second == 0:
        return date.strftime('%Y-%m-%d')
    else:
        return date.strftime('%Y-%m-%d %I:%M %p')

def include(start, end):
    if start == None: return False
    use = end if end else start
    use = datetime.datetime.fromisoformat(use)
    timezone = use.tzinfo
    now = datetime.datetime.now(timezone)
    return use > now
if __name__ == "__main__":
    worklist = TodayActivities()
    print(worklist.fetch())