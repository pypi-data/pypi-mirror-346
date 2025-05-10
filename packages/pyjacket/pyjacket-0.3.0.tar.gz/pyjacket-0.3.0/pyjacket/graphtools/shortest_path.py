import networkx as nx
from scipy.spatial import distance

def max_shortest_path(graph: nx.Graph, endpoints: list[tuple]):
    """Find the pair of endpoints whose shortest path is maximal and return it as a binary image."""
    endpoints = [tuple(yx) for yx in endpoints]
    
    pair, path, path_length = (None, [], -float('inf'))
    for i, p1 in enumerate(endpoints):
        for p2 in endpoints[i+1:]:
            try:
                pair = (p1, p2)
                pth = nx.shortest_path(graph, source=p1, target=p2, weight='weight')
                length = sum(distance.euclidean(pth[k], pth[k+1]) for k in range(len(pth)-1))
                if length > path_length:
                    pair, path, path_length = (pair, pth, length)
            except nx.NetworkXNoPath:
                continue
    return pair, path, path_length
