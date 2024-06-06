# Data used from
# Condense Matter collaboration network: https://snap.stanford.edu/data/ca-CondMat.html
# General Relativity and Quantum Cosmology collaboration network: https://snap.stanford.edu/data/ca-GrQc.html

import multiprocessing
import multiprocessing.dummy
import networkx as nx
import pandas as pd
import time
import random

def calculate_for_existing_edge(subgraph, edge):

  u, v = edge
  neighbors_u = set([n for n in subgraph.neighbors(u)])
  ego_u = nx.ego_graph(subgraph, u, radius=1, undirected=True)
  density_with_node_u = nx.density(ego_u)
  ego_u.remove_node(u)
  density_without_node_u = nx.density(ego_u)
      
  neighbors_v = set([n for n in subgraph.neighbors(v)])
  ego_v = nx.ego_graph(subgraph, v, radius=1, undirected=True)
  density_with_node_v = nx.density(ego_v)
  ego_v.remove_node(v)
  density_without_node_v = nx.density(ego_v)

  common_neigbhours = len(set([n for n in nx.common_neighbors(subgraph, u, v)]))
  total_neigbhours = len(neighbors_u.union(neighbors_v))

  jaccard_coefficient = common_neigbhours / total_neigbhours
  prefferential_attachment = len(neighbors_u) * len(neighbors_v)

  friends_measure = 0
  for x in neighbors_u:
      for y in neighbors_v:
          if subgraph.has_edge(x, y) or x == y:
              friends_measure += 1

  shortest_path = 1 #Always 1 becuase nodes are connected
  link_exists = 1 #Always 1 becuase nodes are connected

  return [u, v, len(neighbors_u), len(neighbors_v), density_with_node_u,
                            density_without_node_u, density_with_node_v, density_without_node_v, common_neigbhours,
                              total_neigbhours, jaccard_coefficient, prefferential_attachment,
                                friends_measure, shortest_path, link_exists]

def calculate_for_non_existing_edge(subgraph, edge):
  u, v = edge
  neighbors_u = set([n for n in subgraph.neighbors(u)])
  ego_u = nx.ego_graph(subgraph, u, radius=1, undirected=True)
  density_with_node_u = nx.density(ego_u)
  ego_u.remove_node(u)
  density_without_node_u = nx.density(ego_u)

  neighbors_v = set([n for n in subgraph.neighbors(v)])
  ego_v = nx.ego_graph(subgraph, v, radius=1, undirected=True)
  density_with_node_v = nx.density(ego_v)
  ego_v.remove_node(v)
  density_without_node_v = nx.density(ego_v)

  common_neigbhours = len(set([n for n in nx.common_neighbors(subgraph, u, v)]))
  total_neigbhours = len(neighbors_u.union(neighbors_v))

  jaccard_coefficient = common_neigbhours / total_neigbhours
  prefferential_attachment = len(neighbors_u) * len(neighbors_v)
  friends_measure = 0
  for x in neighbors_u:
      for y in neighbors_v:
          if subgraph.has_edge(x, y) or x == y:
              friends_measure += 1

  shortest_path = nx.shortest_path_length(subgraph, u, v)
  link_exists = 0 #Always 0 becuase nodes are not connected

  return [u, v, len(neighbors_u), len(neighbors_v), density_with_node_u,
                              density_without_node_u, density_with_node_v, density_without_node_v, common_neigbhours,
                                total_neigbhours, jaccard_coefficient, prefferential_attachment,
                                  friends_measure, shortest_path, link_exists]


start = time.time()

# graph = nx.erdos_renyi_graph(2000, 0.01, directed=False)
# graph = nx.barabasi_albert_graph(2000, 7)
# graph = nx.barabasi_albert_graph
# nx.write_edgelist(graph, path='networks/BarabasAlbert.txt', data=False)
graph = nx.read_edgelist(path='networks/CondMat-Network.txt', comments='#', create_using=nx.Graph(), nodetype=int)
largest = max(nx.connected_components(graph), key=len)
subgraph = graph.subgraph(largest)
print(f'Starting graph, number of nodes {graph.number_of_nodes()} number od edges {graph.number_of_edges()}')
print(f'Largest component, number of nodes {subgraph.number_of_nodes()} number od edges {subgraph.number_of_edges()}')

data = pd.DataFrame(columns=['node_1', 'node_2', 'neighbours_1', 'neighbours_2', 'density_ego_with_node_1',
                        'density_ego_without_node_1', 'density_ego_with_node_2', 'density_ego_without_node_2',
                          'common_neigbhours', 'total_neigbhours', 'jaccard_coefficient', 'prefferential_attachment',
                            'friends_measure', 'shortest_path', 'link_exists'])
results = None
with multiprocessing.Pool() as pool:
    items = [(subgraph, edge) for edge in subgraph.edges()]
    results = [pool.starmap(calculate_for_existing_edge, items)]
    for result in results[0]:
        data.loc[len(data.index)] = result

items = []
nodes = list(subgraph.nodes())
for i in range(len(subgraph.edges())):
    u = random.choice(nodes)
    v = random.choice(nodes)
    while subgraph.has_edge(u, v) or u == v or (u, v) in items or (v, u) in items:
        u = random.choice(nodes)
        v = random.choice(nodes)
    items.append((u, v))
    
with multiprocessing.Pool() as pool:
    prep_items = [(subgraph, edge) for edge in items]
    results = [pool.starmap(calculate_for_non_existing_edge, prep_items)]
    for result in results[0]:
        data.loc[len(data.index)] = result

data.to_csv('data/CondMat.csv', index=False)
end = time.time()
print("Time taken: ", end-start)
