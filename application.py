import flask
from atlassian import Jira
from atlassian import Confluence
import requests
import json

ROTS = ["master","slave","whitelist","blocklist"]
results = []

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/', methods=['GET'])
def home():
    confluence = Confluence(
    url='https://confluence.wip.gapinc.com/',
    username='bprakas',
    password='Mypassword1234(',
    cloud=True)
    spces = confluence.get_all_spaces(start=0, limit=1, expand=None)
    for space in spces["results"]:
        pages= confluence.get_all_pages_from_space(space='cenable', start=0, limit=5, status=None, expand=None, content_type='page')
        for page in pages:
            metadata = {}
            print(page["_links"]["self"])
            suffix = "?expand=body.storage" 
            requestResponse = requests.get(page["_links"]["self"]+suffix, auth=('bprakas', 'Mypassword1234('))
            data = json.loads(requestResponse.text)
            content=data["body"]["storage"]["value"]
            metadata["space_name"]= space["name"]
            metadata["page_name"]= data["title"]
            metadata["page_id"]= data["id"]
            metadata["page_url"]= page["_links"]["self"]
            for ROT in ROTS:
                metadata[ROT]= str(content.count(ROT))
            results.append(metadata)
    return str(results)

app.run()