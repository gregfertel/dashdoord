import requests, json, requests_cache, re
from bs4 import BeautifulSoup as Soup, NavigableString
from xml.etree import ElementTree

requests_cache.install_cache('status_cache', backend='memory', expire_after=90)

def get_subway_status(lines):
    url = "http://web.mta.info/status/serviceStatus.txt"
    try:
        response = requests.get(url)
        content = response.content
        root = ElementTree.fromstring(content)
        data = []
        for line in root[2]:
            d = {}
            for x in line:
                d[x.tag] = x.text
            data.append(d)
        delays = {}
        planned_work = {}
        service_changes = {}
        pattern = '\[(.*?)\]'
        for x in data:
            if x['status'] == 'DELAYS':
                soup = Soup(x['text'], "html5lib")
                if len(soup) == 1:
                    soup = soup.find('body')
                text_i_want = []
                for element in soup:
                    if isinstance(element, NavigableString):
                        text_i_want.append(element)
                    elif element.name == 'b' or element.name == 'p' or element.name == 'strong':
                        text_i_want.append(element.text)
                final_text = "".join(text_i_want).strip()
                for line in re.findall(pattern, final_text):
                    delays[line] = final_text
            elif x['status'] == 'PLANNED WORK':
                soup = Soup(x['text'], "html5lib")
                for br in soup.find_all("br"):
                    br.replace_with("\n")
                work_details = soup.find_all('a', {"class": "plannedWorkDetailLink"})
                for work_detail in work_details:
                    for line in re.findall(pattern, work_detail.text):
                        if line in planned_work:
                            planned_work[line] += "\n" + work_detail.text
                        else:
                            planned_work[line] = work_detail.text
            elif x['status'] == 'SERVICE CHANGE':
                soup = Soup(x['text'])
                text_i_want = []
                for element in soup.body:
                    if element.name == 'p':
                        text_i_want.append(element.text)
                final_text = "".join(text_i_want).strip()
                for line in re.findall(pattern, final_text):
                    service_changes[line] = final_text
        delay_messages = set([])
        planned_work_messages = set([])
        service_change_messages = set([])
        response = {}
        for route in lines:
            if route in delays:
                delay_messages.add(delays[route])
            if route in planned_work:
                planned_work_messages.add(planned_work[route])
            if route in service_changes:
                service_change_messages.add(service_changes[route])
        if delay_messages:
            response['delay_message'] = "\n".join(list(delay_messages))
        if planned_work_messages:
            response['planned_work_message'] = "\n".join(list(planned_work_messages))
        if service_change_messages:
            response['service_change_message'] = "\n".join(list(service_change_messages))
        if response:
            return response
        return False
    except:
        print("Failed, clearing cache")
        requests_cache.clear()
        return False