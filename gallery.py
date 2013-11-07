import re
import webbrowser
import json
from urllib.parse import urljoin
from requests import Session

config = json.load(open('configuration.json'))

session = Session()

if config['login_url']:
	login_data = config['login_data']
	r = session.post(config['login_url'], data=login_data)

def navigate(url, match):
	new_url = urljoin(url, match)
	return [new_url]

def show(url, match):
	webbrowser.open(navigate(url, match)[0])

root = config['root']
str_rules = config['rules']
rules = {}
for key, value in str_rules.items():
	rules[re.compile(key)] = globals()[value]

queue = [root]
processed = set()

while queue:
	url = queue.pop(0)
	processed.add(url)
	page = session.get(url).text

	for regex, function in rules.items():
		for match in regex.findall(page):
			result = function(url, match)
			if result:
				for url in result:
					if url not in processed:
						queue.append(url)
