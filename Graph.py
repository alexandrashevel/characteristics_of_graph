import itertools

import networkx as nx
from operator import itemgetter
import networkx.algorithms.community as nxcom

class graph_custom:
    def __init__(self):
        self.g = 0

    def set_graph(self, gr):
        self.g = gr

    def get_diameter(self):
        return str(nx.diameter(self.g.to_undirected()))

    def get_density(self):
        return str(nx.density(self.g))

    def get_average_clustering(self):
        G = nx.DiGraph()
        for u, v in self.g.edges():
            if G.has_edge(u, v):
                G[u][v]['weight'] += 1
            else:
                G.add_edge(u, v, weight=1)
        return str(nx.average_clustering(G))

    def get_average_shortest_path_length(self):
        return str(nx.average_shortest_path_length(self.g))

    def get_max_clustering(self):
        G = nx.DiGraph()
        for u, v in self.g.edges():
            if G.has_edge(u, v):
                G[u][v]['weight'] += 1
            else:
                G.add_edge(u, v, weight=1)
        return str(list(sorted(nx.clustering(G).items(), key=itemgetter(1), reverse=True))[0][1])

    def get_betweenness_centrality(self):
        G = nx.DiGraph()
        for u, v in self.g.edges():
            if G.has_edge(u, v):
                G[u][v]['weight'] += 1
            else:
                G.add_edge(u, v, weight=1)
        return str(list(sorted(nx.betweenness_centrality(G).items(), key=itemgetter(1), reverse=True))[0][0])

    def get_degree_centrality(self):
        return str(list(sorted(nx.degree_centrality(self.g).items(), key=itemgetter(1), reverse=True))[0][0])

    def get_closeness_centrality(self):
        return str(list(sorted(nx.closeness_centrality(self.g).items(), key=itemgetter(1), reverse=True))[0][0])

    def get_density(self):
        return nx.density(self.g)

    def get_comminity(self):
        return sorted(nxcom.greedy_modularity_communities(self.g.to_undirected()), key=len, reverse=True)

    def get_number_connected_components(self):
        return nx.number_connected_components(self.g)

    def get_average_node_connectivity(self):
        return nx.average_node_connectivity(self.g)

    def get_network_community(self):
        return sorted(nxcom.greedy_modularity_communities(self.g), key=len, reverse=True)

    def read_from_file(self, filename):
        self.g = nx.read_pajek(filename)
