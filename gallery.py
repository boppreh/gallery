import re
import webbrowser
from urllib.parse import urljoin
from requests import Session
from os import path

def navigate(url, match, session):
	new_url = urljoin(url, match)
	return [new_url]

def show(url, match, session):
    full_url = urljoin(url, match)
    webbrowser.open(full_url)

def download(url, match, session):
    full_url = urljoin(url, match)
    with open(path.join('cache', path.basename(full_url)), 'wb') as f:
        request = session.get(full_url, stream=True)

        for block in request.iter_content(1024):
            if not block:
                break

            f.write(block)

def save(url, match, session):
    filename = path.join('cache', 'saved_text.txt')
    with open(filename, 'a', encoding='utf-8') as f:
        f.write(match)

def echo(url, match, session):
    print(match)


def run(root, rules, session):
    queue = [root]
    processed = set()

    while queue:
        url = queue.pop(0)
        if url in processed:
            continue
        processed.add(url)
        page = session.get(url).text

        for regex, function in rules.items():
            for match in regex.findall(page):
                result = function(url, match, session) or []
                queue.extend(result)

if __name__ == '__main__':
    import json
    config = json.load(open('configuration.json'))

    root = config['root']
    str_rules = config['rules']
    rules = {}
    for key, value in str_rules.items():
        rules[re.compile(key)] = globals()[value]

    session = Session()

    if 'login_url' in config:
        login_data = config['login_data']
        r = session.post(config['login_url'], data=login_data)

    run(root, rules, session)

