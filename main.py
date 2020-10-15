from natasha import Segmenter, MorphVocab, NewsEmbedding, NewsMorphTagger, NewsSyntaxParser, NewsNERTagger, Doc
import matplotlib.pyplot as plt
import math
import numpy as np
import networkx as nx

segmenter = Segmenter()
morph_vocab = MorphVocab()

emb = NewsEmbedding()
morph_tagger = NewsMorphTagger(emb)
syntax_parser = NewsSyntaxParser(emb)
ner_tagger = NewsNERTagger(emb)

with open("news.txt") as newsfile:
    news = newsfile.read().split('=====\n')[1:]

locations = {}
organizations = {}
connections = {}

for article in news:
    doc = Doc(article)
    doc.segment(segmenter)
    doc.tag_morph(morph_tagger)
    doc.tag_ner(ner_tagger)

    for token in doc.tokens:
        token.lemmatize(morph_vocab)
    for span in doc.spans:
        span.normalize(morph_vocab)
        
    loc = []
    org = []
    for span in doc.spans:
        if span.type == 'LOC':
            locations[span.normal] = locations.get(span.normal, 0) + 1
            loc.append(span.normal)
        if span.type == 'ORG':
            organizations[span.normal] = organizations.get(span.normal, 0) + 1
            if span.normal not in connections.keys():
                connections[span.normal] = {}
            org.append(span.normal)
            
    for location in loc:
        for organization in org:
            connections[organization][location] = connections[organization].get(location, 0) + 1

G = nx.Graph()
for org in connections.keys():
    for loc in connections[org].keys():
        G.add_edge(org, loc)

all_nodes = {**locations, **organizations}

pstn = nx.spring_layout(G)
sz = [all_nodes[n] for n in G.nodes]

lw = []
for e in G.edges:
    if e[0] in connections.keys() and e[1] in connections[e[0]].keys():
        lw.append(math.log(connections[e[0]][e[1]], 10) + 1)
    else:
        lw.append(math.log(connections[e[1]][e[0]], 10) + 1)

nx.draw(G, pos = pstn, node_color = 'b', edge_color = 'g', with_labels = True, node_size = sz, width = lw)

probable_places = {} #самый вероятный адрес для организации
    for org in connections.keys():
        probable_places[org] = ''
    for loc in connections[org].keys():
        if probable_places[org] == '':
            probable_places[org] = loc
        if connections[org][loc] > connections[org][probable_places[org]]:
            probable_places[org] = loc
