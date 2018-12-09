import networkx as net
from networkx.algorithms import bipartite
import matplotlib.pyplot as plot
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
import re
import pandas as pd
import numpy as np
import random
import time
import datetime

# define function to iterate through friends list
def get_friends(g, center):
    driver.get('https://www.facebook.com/' + center + '/friends')
    time.sleep(random.choice(range(100, 300)) / 100)

    friends_df = pd.DataFrame({'user_name': [], 'user_id': []})

    # load more friends until all are loaded
    # try:
    #     friends_n = driver.find_element_by_class_name('_3d0').text
    #     refresh_n = int(np.ceil(int(friends_n)/20))
    # except:
    #     refresh_n = 20  # default to 20 if number of friends is private
    # for i in range(refresh_n):
    #     actions.send_keys(Keys.END)
    #     actions.perform()
    #     time.sleep(random.choice(range(120, 180)) / 100)

    full_friends_list = driver.find_element_by_class_name('_5h60')
    sub_friends_list = full_friends_list.find_elements_by_class_name('uiList')

    row = 0
    for i in range(len(sub_friends_list)):
        friend_container_list = sub_friends_list[i].find_elements_by_class_name('_698')
        for j in range(len(friend_container_list)):
            friend_container = sub_friends_list[i].find_elements_by_class_name('_698')[j]
            friend_user_name = friend_container.find_elements_by_class_name('fsl')[0].text
            friend_href = friend_container.find_elements_by_class_name('_5q6s')[0].get_attribute('href')
            if friend_href is not None:
                friend_user_id = re.search("https://www.facebook.com/(.+?)\?", friend_href).group(1)
                g.add_edge(center, friend_user_id)  # add the edge to the network
                friends_df.loc[row, ['user_name', 'user_id']] = [friend_user_name, friend_user_id]
                print('%d: %s' % (row, friend_user_id))
                row += 1

    # get attributes for center node
    # info_dict = get_attr(center)
    # for key, value in info_dict.items():
    #     g.node[center][key] = value


# define function to get attributes of friends
def get_attr(center):
    driver.get('https://www.facebook.com/' + center + '/about')
    time.sleep(random.choice(range(300, 700)) / 100)

    info_dict = {}
    # get contact info and birthday if available
    for i in range(1, 5):
        try:
            info = driver.find_element_by_css_selector('._2pif:nth-child(' + str(i) + ') ._ikh , ._2pif:nth-child(5) ._2ieq div').text
            info = info.split('\n')
            info_dict[info[0]] = info[1]
        except:
            pass

    # get workplace, school and home if available
    for i in range(0, 8):
        try:
            info = driver.find_elements_by_css_selector('._5y02 , ._2pi4')[i].text
            if info[0:4] == 'Work':
                info_dict['Work'] = info
            if info[0:4] == 'Stud':
                info_dict['Study'] = info
            if info[0:4] == 'Live':
                info_dict['Live'] = info
        except:
            pass

    print(center, info_dict)
    return info_dict


# define function to get likes of friends
def get_likes(center):
    driver.get('https://www.facebook.com/' + center + '/likes')
    time.sleep(random.choice(range(300, 700)) / 100)

    info_dict = {}
    try:
        likes = driver.find_element_by_xpath('//*[@id="pagelet_timeline_medley_likes"]/div[1]/div[2]/div[1]')
        likes_list = likes.find_elements_by_class_name('_3c_')
        for e in likes_list[1:]:  # skip all likes
            info = re.split("(\d+)", e.text)
            info_dict['Like: ' + info[0]] = info[1]
    except:
        pass

    print(center, info_dict)
    return info_dict


# define function to sample network thru snowball sampling
def snowball_sample(g, center, max_depth=1, current_depth=0, taboo_list=[]):
    print(center, current_depth, max_depth, taboo_list)
    print('number of nodes: %d' % len(g))
    net.write_pajek(g, '/Users/brucehao/Desktop/facebook_network.net')
    if current_depth == max_depth:
        # if we have reached the depth limit of the search, return
        print('out of depth')
        return taboo_list
    if center in taboo_list:
        # we've been here before -- return right away
        return taboo_list
    else:
        taboo_list.append(center)  # we shall never return to the same node

    get_friends(g, center)

    for node in g.neighbors(center):
        # iterate through all friends of central node, call snowball_sample recursively
        taboo_list = snowball_sample(g, node, current_depth=current_depth+1,
                                     max_depth=max_depth, taboo_list=taboo_list)
    return taboo_list


# def function to trim nodes from network
def trim_degrees(g, degree=1):
    g2=g.copy()
    d=net.degree(g2)
    for n in list(g2.nodes()):
        if d[n]<=degree: g2.remove_node(n)
    return g2


# def function to add attributes to trimmed network
def add_attr(g2):
    g3=g2.copy()
    for node in g3:
        info_dict = get_attr(node)
        for key, value in info_dict.items():
            g3.node[node][key] = value
    return g3


# def function to show network graph
def show_network(g3):
    pos = net.spring_layout(g3)
    net.draw_networkx_nodes(g3, pos, alpha=0.5)
    net.draw_networkx_edges(g3, pos, alpha=0.3)
    net.draw_networkx_labels(g3, pos, alpha=0.7)


'''
Customized read and write pajek functions to handle
'''
def generate_pajek_(G):
    import warnings
    from networkx.utils import is_string_like, open_file, make_str

    if G.name == '':
        name = 'NetworkX'
    else:
        name = G.name
    # Apparently many Pajek format readers can't process this line
    # So we'll leave it out for now.
    # yield '*network %s'%name

    # write nodes with attributes
    yield '*vertices %s' % (G.order())
    nodes = list(G)
    # make dictionary mapping nodes to integers
    nodenumber = dict(zip(nodes, range(1, len(nodes) + 1)))
    for n in nodes:
        # copy node attributes and pop mandatory attributes
        # to avoid duplication.
        na = G.nodes.get(n, {}).copy()
        x = na.pop('x', 0.0)
        y = na.pop('y', 0.0)
        id = int(na.pop('id', nodenumber[n]))
        nodenumber[n] = id
        shape = na.pop('shape', 'ellipse')
        s = ' '.join(map(make_qstr, (id, n, x, y, shape)))
        # only optional attributes are left in na.
        for k, v in na.items():
            if is_string_like(v) and v.strip() != '':
                s += ' %s %s' % (make_qstr(k), make_qstr(v))
            else:
                warnings.warn('Node attribute %s is not processed. %s.' %
                              (k,
                               'Empty attribute' if is_string_like(v) else
                               'Non-string attribute'))
        s = s.replace('\n', ' ')
        yield s

    # write edges with attributes
    if G.is_directed():
        yield '*arcs'
    else:
        yield '*edges'
    for u, v, edgedata in G.edges(data=True):
        d = edgedata.copy()
        value = d.pop('weight', 1.0)  # use 1 as default edge value
        s = ' '.join(map(make_qstr, (nodenumber[u], nodenumber[v], value)))
        for k, v in d.items():
            if is_string_like(v) and v.strip() != '':
                s += ' %s %s' % (make_qstr(k), make_qstr(v))
                s += ' '
            else:
                warnings.warn('Edge attribute %s is not processed. %s.' %
                              (k,
                               'Empty attribute' if is_string_like(v) else
                               'Non-string attribute'))
        yield s



def write_pajek_(G, path, encoding='UTF-8'):
    f = open(path, 'w')
    for line in generate_pajek_(G):
        line += '\n'
        f.write(line)  # line.encode(encoding))
    f.close()



def read_pajek_(path, encoding='UTF-8'):
    lines = open(path, 'r')
    return parse_pajek_(lines)



def parse_pajek_(lines):
    import shlex
    import networkx as nx
    from networkx.utils import is_string_like, open_file, make_str
    # multigraph=False
    if is_string_like(lines):
        lines = iter(lines.split('\n'))
    lines = iter([line.rstrip('\n') for line in lines])
    G = nx.MultiDiGraph()  # are multiedges allowed in Pajek? assume yes
    labels = []  # in the order of the file, needed for matrix
    while lines:
        try:
            l = next(lines)
        except:  # EOF
            break
        if l.lower().startswith("*network"):
            try:
                label, name = l.split(None, 1)
            except ValueError:
                # Line was not of the form:  *network NAME
                pass
            else:
                G.graph['name'] = name
        elif l.lower().startswith("*vertices"):
            nodelabels = {}
            l, nnodes = l.split()
            for i in range(int(nnodes)):
                l = next(lines)
                try:
                    splitline = [x.decode('utf-8') for x in
                                 shlex.split(make_str(l).encode('utf-8'))]
                except AttributeError:
                    splitline = shlex.split(str(l))
                id, label = splitline[0:2]
                labels.append(label)
                G.add_node(label)
                nodelabels[id] = label
                G.nodes[label]['id'] = id
                try:
                    x, y, shape = splitline[2:5]
                    G.nodes[label].update({'x': float(x),
                                           'y': float(y),
                                           'shape': shape})
                except:
                    pass
                extra_attr = zip(splitline[5::2], splitline[6::2])
                G.nodes[label].update(extra_attr)
        elif l.lower().startswith("*edges") or l.lower().startswith("*arcs"):
            if l.lower().startswith("*edge"):
                # switch from multidigraph to multigraph
                G = nx.MultiGraph(G)
            if l.lower().startswith("*arcs"):
                # switch to directed with multiple arcs for each existing edge
                G = G.to_directed()
            for l in lines:
                try:
                    splitline = [x.decode('utf-8') for x in
                                 shlex.split(make_str(l).encode('utf-8'))]
                except AttributeError:
                    splitline = shlex.split(str(l))

                if len(splitline) < 2:
                    continue
                ui, vi = splitline[0:2]
                u = nodelabels.get(ui, ui)
                v = nodelabels.get(vi, vi)
                # parse the data attached to this edge and put in a dictionary
                edge_data = {}
                try:
                    # there should always be a single value on the edge?
                    w = splitline[2:3]
                    edge_data.update({'weight': float(w[0])})
                except:
                    pass
                    # if there isn't, just assign a 1
#                    edge_data.update({'value':1})
                extra_attr = zip(splitline[3::2], splitline[4::2])
                edge_data.update(extra_attr)
                # if G.has_edge(u,v):
                #     multigraph=True
                G.add_edge(u, v, **edge_data)
        elif l.lower().startswith("*matrix"):
            G = nx.DiGraph(G)
            adj_list = ((labels[row], labels[col], {'weight': int(data)})
                        for (row, line) in enumerate(lines)
                        for (col, data) in enumerate(line.split())
                        if int(data) != 0)
            G.add_edges_from(adj_list)

    return G



def make_qstr(t):
    """Return the string representation of t.
    Add outer double-quotes if the string has a space.
    """
    if not is_string_like(t):
        t = str(t)
    if " " in t:
        t = r'"%s"' % t

    return t


'''
functions to cleanse certain attributes
'''
# parse g3 graph Study attribute for schools attended
def cleanse_school_list(g3):
    schools_list = []
    friends_list = []
    for friend in list(g3.nodes):
        try:
            if g3.node[friend]['Study'] not in schools_list:
                schools_list.append(g3.node[friend]['Study'])
                friends_list.append(friend)
        except:
            pass

    schools_list_clean = []
    for study in schools_list:
        # most recent school
        study = re.sub(r"Jan |Feb |Mar |Apr |May |Jun |Jul |Aug |Sep |Oct |Nov |Dec ", "", study)
        if len(re.findall("(Past:|Class of|\d{4} to)", study)) == 0:
            school = re.findall(" at (.*)", study)
            schools_list_clean.append(school[0])
        else:
            school = re.findall(" at (.*)\s(Past:|Class of|\d{4} to)", study)
            schools_list_clean.append(school[0][0])
        # previously attended schools
        if len(re.findall(" Past: (.*)", study)) > 0:
            study_and = re.findall(" Past: (.*)", study)
            if len(re.findall("(.*) and (.*)", study_and[0])) > 0:
                schools_list_clean.append(re.findall("(.*) and (.*)", study_and[0])[0][0])
                schools_list_clean.append(re.findall("(.*) and (.*)", study_and[0])[0][1])
            else:
                schools_list_clean.append(study_and[0])
    schools_list_clean = list(set(schools_list_clean))
    return(schools_list_clean)


# parse g3 graph Live attribute for places lived
def cleanse_resid_list(g3):
    resid_list = []
    friends_list = []
    for friend in list(g3.nodes):
        try:
            if g3.node[friend]['Live'] not in resid_list:
                resid_list.append(g3.node[friend]['Live'])
                friends_list.append(friend)
        except:
            pass

    resid_list_clean = []
    for resid in resid_list:
        # most recent place lived
        if len(re.findall(" From ", resid)) == 0:
            resid = re.findall(" in (.*)", resid)
            resid_list_clean.append(resid[0])
        else:
            resid = re.findall("in (.*)\sFrom\s(.*)", resid)
            resid_list_clean.append(resid[0][0])
    resid_list_clean = list(set(resid_list_clean))
    return (resid_list_clean)


# parse g3 graph Live attribute for year of birth
def cleanse_yob_list(g3):
    yob_list = []
    friends_list = []
    for friend in list(g3.nodes):
        try:
            if g3.node[friend]['Birthday'] not in yob_list:
                yob_list.append(g3.node[friend]['Birthday'])
                friends_list.append(friend)
        except:
            pass

    yob_list_clean = []
    for yob in yob_list:
        # most recent place lived
        if len(re.findall(", ", yob)) != 0:
            yob = re.findall(",\s(.*)", yob)
            yob_list_clean.append(yob[0])
    yob_list_clean = list(set(yob_list_clean))
    return (yob_list_clean)

