import requests, json, requests_cache, re
from bs4 import BeautifulSoup as Soup, NavigableString
from xml.etree import ElementTree

requests_cache.install_cache('status_cache', backend='memory', expire_after=180)

def get_subway_status(lines):
    url = "http://web.mta.info/status/serviceStatus.txt"
    response = requests.get(url)
    content = response.content
    print content
    root = ElementTree.fromstring(content)
    data = []
    for line in root[2]:
        d = {}
        for x in line:
            d[x.tag] = x.text
        data.append(d)
    delays = {}
    for x in data:
        if x['status'] == 'DELAYS':
            soup = Soup(x['text'])
            text_i_want = []
            for element in soup:
                if isinstance(element, NavigableString):
                    text_i_want.append(element)
                elif element.name == 'b' or element.name == 'p':
                    text_i_want.append(element.text)
            final_text = "".join(text_i_want).strip()
            pattern = '\[(.*?)\]'
            for line in re.findall(pattern, final_text):
                delays[line] = final_text
    status_messages = set([])
    for route in lines:
    	if route in delays:
    		status_messages.add(delays[route])
    if status_messages:
        return " ".join(list(status_messages))
    else:
        return False