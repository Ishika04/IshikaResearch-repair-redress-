## import python libraries to load csv
import pandas as pd
import io
import requests

## import python libraries to create the chart
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np

## import python libraries to conver the csv to json
import json

## retrieve data from google doc and convert to csv
URL = 'https://docs.google.com/spreadsheets/d/1mZHQ1Rz0aViNyLFrQmFGwNUt4CoByB3FmMlPxKVOMGk/gviz/tq?tqx=out:csv&sheet=sample_people_doc'
s = requests.get(URL).content
people_data = pd.read_csv(io.StringIO(s.decode('utf-8')))

## create a dataframe with just the tags
tag_data = people_data
tag_data = tag_data.drop(['Name'], axis=1)

## create final files
final_json = '{"nodes": ['
nodes = []
links = []

## get the number of columns & rows for tags
num_columns = len(tag_data.columns)
num_rows = len(tag_data.index)

## create the nodes portion of the json 
for i in people_data.index:
    row_json = ""
    row_json = '{"id": "' + str(people_data.loc[i,"Name"]) +'"' ##make name the id

    tags = [] ##tags for a specific row
    ## in a given row, iterate through the columns to add to the tags dict
    for h in range(num_columns):
        if (tag_data.iat[i, h] == True):
            tags.append(1)
        else:
            tags.append(0)

    ## Percentages for each circle
    total_num = sum(tags)
    percentage = 100 / total_num
    
    ## Find the colors
    colors = []
    current_num = 1
    for value in tags:
        if (value == 1):
            colors.append(current_num)
        current_num = current_num + 1

    ## generate the piechart string
    piechart_string = '"pieChart" : ['
    for r in range(len(colors)):
        current_string = '{ "color" : ' + str(colors[r]) + ', "percent" : ' + str(percentage) + ' }'
        if (r != total_num - 1):
            current_string = current_string + ','
        piechart_string = piechart_string + current_string

    piechart_string = piechart_string + ']}'

    if (i != len(people_data.index) - 1):
        piechart_string = piechart_string + ','

    row_json = row_json + ', ' + piechart_string

    final_json = final_json + row_json


## create the links portion of the json
final_json = final_json + '],"links": ['

## Cornell connections
cornell_connections = people_data[people_data['Cornell'] == True]
cornell_json = ''

cornell_names = cornell_connections['Name'].tolist() ##turn name column into a list
list_length = len(cornell_names) - 1
list_index = 1
prev_listindex = 1

for item in cornell_names:
    for val in range(list_length):
        row_json = '{"source": "' + str(item) + '", "target": "' + str(cornell_names[list_index]) + '"},'
        list_index = list_index + 1
        cornell_json = cornell_json + row_json
    list_length = list_length - 1
    prev_listindex = prev_listindex + 1
    list_index = prev_listindex

## EDGI connections
edgi_connections = people_data[people_data['EDGI'] == True]
edgi_json = ''

edgi_names = edgi_connections['Name'].tolist() ##turn name column into a list
list_length = len(edgi_names) - 1
list_index = 1
prev_listindex = 1

for item in edgi_names:
    for val in range(list_length):
        row_json = '{"source": "' + str(item) + '", "target": "' + str(edgi_names[list_index]) + '"},'
        list_index = list_index + 1
        edgi_json = edgi_json + row_json
    list_length = list_length - 1
    prev_listindex = prev_listindex + 1
    list_index = prev_listindex

## Public Lab connections
public_connections = people_data[people_data['Publiclab'] == True]
public_json = ''

public_names = public_connections['Name'].tolist() ##turn name column into a list
list_length = len(public_names) - 1
list_index = 1
prev_listindex = 1

for item in public_names:
    for val in range(list_length):
        row_json = '{"source": "' + str(item) + '", "target": "' + str(public_names[list_index]) + '"},'
        list_index = list_index + 1
        public_json = public_json + row_json
    list_length = list_length - 1
    prev_listindex = prev_listindex + 1
    list_index = prev_listindex

## LittleSis connections
sis_connections = people_data[people_data['LittleSis'] == True]
sis_json = ''

sis_names = sis_connections['Name'].tolist() ##turn name column into a list
list_length = len(sis_names) - 1
list_index = 1
prev_listindex = 1

for item in sis_names:
    for val in range(list_length):
        row_json = '{"source": "' + str(item) + '", "target": "' + str(sis_names[list_index]) + '"},'
        list_index = list_index + 1
        sis_json = sis_json + row_json
    list_length = list_length - 1
    prev_listindex = prev_listindex + 1
    list_index = prev_listindex

final_json = final_json + cornell_json + edgi_json + public_json + sis_json
final_json = final_json[:-1] + ']}'

print(final_json)

# creating json file
# the JSON file is named as test1
# out_file = open("test1.json", "w")
# json.dump(final_json, out_file, indent = 4, sort_keys = False)
# out_file.close()

# #############  SAMPLE GRPAH CODE ###############
# # parameters for pie plot
# radius = 0.2
# cmap = plt.cm.viridis

# # make graph
# G = nx.Graph()
# nodes = [1,2,3,4]
# edges = ((1,2),(3,2),(1,4),(3,4))
# G.add_nodes_from(nodes)
# G.add_edges_from(edges)
# pos = nx.spring_layout(G)

# # storing attributes in a dict
# attrs = {
#     1:[1,1,1],
#     2:[0.5, 1, 0],
#     3:[0, 0.6, 0],
#     4:[0.5, 1, 0.5],
# }

# # normalising data to make colors
# a = np.array(list(attrs.values()))
# maxes = np.max(a, axis=0) # note that this will throw an error if different nodes have different number of features. 

# # collect colors in dictionary    
# colors= {}

# for key, val in attrs.items():
#     colors[key] = list(np.array(val)/maxes)

# # draw graph and draw pieplots instead of nodes
# nx.draw_networkx_edges(G, pos=pos)
# for node in G.nodes:

#     attributes = attrs[node]

#     a = plt.pie(
#         [1]*len(attributes), # s.t. all wedges have equal size
#         center=pos[node], 
#         colors = [cmap(a) for a in colors[node]],
#         radius=radius)

# plt.ylim(-2,2)
# plt.xlim(-2,2)
# plt.show()