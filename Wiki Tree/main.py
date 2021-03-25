import requests
from bs4 import BeautifulSoup
from anytree import Node, RenderTree
import json
from os import system

import pydot
# rankdir="RL"

cache = {}

graph = pydot.Dot('my_graph', graph_type='graph', ranksep=3, ratio="auto", rankdir="RL")

blocklist = ["Help:IPA", "#cite_note", "File", "upload", "wiktionary", "geohack"]

def check_valid(link):
    for block in blocklist:
        if block in link:
            return False
    return True

def calc_total(depth, breadth):
    total = 0
    for i in range(depth):
        total += breadth ** i
    return total

def link_to_title(link):
    link = link.split("/")[-1]
    link = link.replace("_", " ")
    return link

def get_links(url):
    links = []
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        p_tags = soup.find_all("div", {"class": "mw-parser-output"})[0].find_all("p")
    except:
        return links

    for p in p_tags:
        try:
            a = p.find_all("a")
            for A in a:
                if check_valid(A.get("href")):
                    links.append(A.get("href"))
        except:
            pass # P has no links in it, ignore
    return links


# find_page("http://google.com")

def calc_tree(url, parent, depth, breadth):
    if(parent == 0):
        color = "red"
    else:
        color = "black"
    graph.add_node(pydot.Node(link_to_title(url), color=color))
    if(parent != 0):
        graph.add_edge(pydot.Edge(pydot.Node(link_to_title(url)), pydot.Node(link_to_title(parent)), color='blue'))

    if depth > 0:
        print(url)
        links = get_links(url) # no links in it, ignore
        # print(links)
        i = 0
        limit = 0
        if breadth < len(links):
            limit = breadth
        else:
            limit = len(links)
        while i < limit:
            link = "https://en.wikipedia.org" + links[i]
            # print(link)
            calc_tree(link, url, depth -1, breadth)
            i+=1
        return 
    else:
        return "Done"

link = "https://en.wikipedia.org/wiki/Bourne_Grammar_School"

print(calc_total(3, 10))

calc_tree(link, 0, 3, 10)
graph.write_png('output.png')

# graph.write_dot('output_graphviz.dot')
# system("twopi output_graphviz.dot -Tpng -O")