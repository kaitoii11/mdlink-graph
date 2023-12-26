#/usr/bin/env python

import os
import sys
import re
import pathlib
import markdown
from bs4 import BeautifulSoup
import graphviz


path = sys.argv[1:]
dot = graphviz.Digraph()

url_pattern = re.compile("http[s]?://")


for file in path:
    print(os.path.isfile(file))
    if not os.path.isfile(file) or not pathlib.Path(file).suffix == '.md':
        continue

    with open(file,'r') as f:
       text = f.read()

    soup = BeautifulSoup(markdown.markdown(text), 'html.parser')

    filename = os.path.basename(file).replace('.md','')
    dot.node(filename)

    for a in soup.find_all('a', href=True):
        link = a['href']
        if not url_pattern.match(link):
            link = a['href'].replace('/','')
            dot.edge(filename, link)

print(dot.source)
dot.view()
