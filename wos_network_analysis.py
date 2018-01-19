# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import community
from networkx.algorithms.community import asyn_lpa


__author__ = """ Lei YIN (lyneoma@gmail.com); Shikun LI (15063425220@163.com) """


def plot_communities():

    size = float(len(set(partition.values())))
    pos = nx.spring_layout(G)

    colors = ["#FF0000", "#000000", "#0000FF", "#FFFF00", "#00FFFF", "#FF00FF",
              "#C0C0C0", "#808080", "#800000", "#808000", "#008000", "#800080", "#6B8E23"]
    count = 0
    for com in set(partition.values()):
        count += 1
        list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == com]
        print(count / size)
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size=50, node_color=colors[count - 1])
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    nx.write_gml(G, "test.gml")
    plt.show()

if __name__ == "__main__":

    adj_file = "test.adjlist"
    G = nx.read_adjlist(adj_file)

    # Louvain algorithm
    partition = community.best_partition(G)
    print(partition)

    # TODO Evaluation of Louvain algorithm

    # Label Propagation Algorithm
    cs = asyn_lpa.asyn_lpa_communities(G)
    print(list(cs))

    # TODO Evaluation of Label Propagation Algorithm

    # TODO implement Smart local moving method
    # TODO Evaluation of Smart local moving

    # TODO implement Infomap method
    # TODO Evaluation of Infomap


