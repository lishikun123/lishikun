# -*- coding: utf-8 -*-

import networkx as nx
import community
from networkx.algorithms.community import asyn_lpa
from networkx.algorithms.community.quality import modularity, coverage


__author__ = """ Lei YIN (lyneoma@gmail.com); Shikun LI (15063425220@163.com) """


if __name__ == "__main__":

    adj_file = "test.adjlist"
    graph = nx.read_adjlist(adj_file)

    """
        Louvain algorithm and Evaluation
    """
    partition = community.best_partition(graph)

    # Modularity
    mod = community.modularity(partition, graph)
    print(mod)

    # TODO Conductance of Louvain
    # TODO Coverage of Louvain
    # TODO Adjusted Rand Index of Louvain
    # TODO Normalized Mutual Information of Louvain
    # TODO Normalized Mutual Information Variant of Louvain

    """
        Label Propagation Algorithm and Evaluation
    """
    cs = asyn_lpa.asyn_lpa_communities(graph)

    # Modularity
    mod = modularity(cs, graph)
    print(mod)

    # Coverage
    cov = coverage(cs, graph)
    print(cov)

    # TODO Conductance of Label Propagation
    # TODO Adjusted Rand Index of Label Propagation
    # TODO Normalized Mutual Information of Label Propagation
    # TODO Normalized Mutual Information Variant of Label Propagation

    # TODO implement Smart local moving method
    # TODO Evaluation of Smart local moving

    # TODO implement Infomap method
    # TODO Evaluation of Infomap




