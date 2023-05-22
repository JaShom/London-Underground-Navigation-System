import heapq
class Graph:
    def __init__(self, edges, nodes, weights):
        self.edges = edges
        self.nodes = [node for node in nodes[1]]
        self.weights = weights
        
    
    def dijkstraPath(self, start, end):
        adj = {i:[] for i in self.nodes}

        # Allowing edges to be bi-directional since one could go forward and backwards on a train line.
        for src, dst, wei, line in self.edges:
            adj[src].append([dst, wei, line])
            adj[dst].append([src, wei, line])
        

        shortest = {}
        minHeap = [(0, start, 0, "")]
        path = []
        time_of_path = []

        while minHeap:
            w1, n1, par, lin = heapq.heappop(minHeap) # Weight, Node, Parent, Station Line
            if n1 in shortest:
                continue
            shortest[n1] = [w1, par, lin] # Node is the key for the rest of the variables

            if n1 == end: # Reached destination, shortest will look messy as other paths were being used too
                # Time to the path we're looking for by going backwards via parents
                tmp = n1
                while par != start:
                    path.append([tmp, shortest[tmp][2], shortest[tmp][0]])
                    if (par, tmp) in self.weights:
                        time_of_path.append(self.weights[(par, tmp)])
                    tmp = par
                    par = shortest[par][1]
                    
                path.append([tmp, shortest[tmp][2], shortest[tmp][0]])
                time_of_path.append(self.weights[(par, tmp)])
                path.append([par, shortest[tmp][2], 0])
                path.reverse()
                time_of_path.reverse()
                return path, shortest[n1][0], time_of_path

            for n2, w2, li in adj[n1]:
                if n2 not in shortest:
                    heapq.heappush(minHeap, (w1 + w2 + 1, n2, n1, li)) # Included the 1 minute wait time between stations here