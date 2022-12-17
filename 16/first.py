import re
import math
import networkx as nx
import itertools
import functools


# Note: gotta play with the heuristic thresholds


# Idea:
# 1. Build graph with 1-weighted edges
# 2. add short-cut edges with weight >1 to skip 0-flow_rate vertices
# 3. remove 0-flow_rate vertices (except starting point AA)
# 4. Floyd-Warshall all-pairs shortest paths
# 5. Make complete graph by adding edges with weights from 4.
# 6. brute force with heuristics (pruning, highest-value-first, etc)

# general things:
# - Assuming that visting a node == opening a node, which is not always optimal
#       (but most of the time since 0-flow_rate vertices are gone)
# - Add scores for all incoming minutes upon opening a valve
# - Start with "AA" "opened" because that is the only flow_rate==0 that didn't get removed


### part 1
# $ time python3.8 first.py
# silver: 1915
#
# real	0m0.186s
# user	0m0.174s
# sys	0m0.012s

### part 2
# $ time pypy3 second.py
# gold: 2772
#
# real	0m10.860s
# user	0m10.800s
# sys	0m0.028s




with open("input.txt", "r") as f:
    lines = f.read().splitlines()


class Vertex:
    def __init__(self, id, flow_rate):
        self.flow_rate = flow_rate
        self.id = id
        self.edges = {self}
        self.edge_weights = {self: 1}

    def add_edge(self, dst_v, weight):
        self.edges.add(dst_v)
        self.edge_weights[dst_v] = weight


    def __repr__(self):
        return self.id
        # return str(self.id) + ": edges="\
        #        + str([e.id for e in self.edges])\
        #        + " weights=" + str({v.id: weight for v, weight in self.edge_weights.items()})

def visualize_graph(G, filename):
    A = nx.Graph()
    for vertex in G.values():
        A.add_node(vertex.id, label=str(vertex.flow_rate)+" - "+vertex.id)
        for to_vertex in vertex.edges:
            weight = vertex.edge_weights[to_vertex]
            A.add_edge(vertex.id, to_vertex.id, weight=weight)
            edge = A.get_edge_data(vertex.id, to_vertex.id)
            edge['label'] = weight

    #nx.spring_layout(A)
    B = nx.drawing.nx_pydot.to_pydot(A)
    B.write_png(filename, prog="dot")
    #B.write_png(filename, prog=["neato", "-Goverlap=false"])


### build graph
G = {}
# gather data
data = []
for line in lines:
    res = re.search(r'Valve (.*?) has flow rate=(.*?); tunnels? leads? to valves? (.*?)$', line)
    valve_id, flow_rate, to_valves = res.groups()
    to_valves = to_valves.split(", ")
    data.append((valve_id, int(flow_rate), to_valves))

# add vertices
for valve_id, flow_rate, to_valves in data:
    v = Vertex(valve_id, flow_rate)
    G[valve_id] = v

# add edges
for valve_id, flow_rate, to_valves in data:
    for to_valve_id in to_valves:
        G[valve_id].add_edge(G[to_valve_id], 1)


#visualize_graph(G, "input_step1.png")

# add short-cut edges with weight >1 to skip 0-flow_rate vertices
zero_flow_state_vertices = set([vertex for vertex in G.values() if vertex.flow_rate == 0])
for vertex in zero_flow_state_vertices:
    for neighbor1 in vertex.edges:
        for neighbor2 in vertex.edges:
            weight = vertex.edge_weights[neighbor1] + vertex.edge_weights[neighbor2]
            weight = min(weight,
                         neighbor1.edge_weights.get(neighbor2, math.inf),
                         neighbor2.edge_weights.get(neighbor1, math.inf))
            neighbor1.add_edge(neighbor2, weight)
            neighbor2.add_edge(neighbor1, weight)

#visualize_graph(G, "input_step2.png")

# remove 0-flow_rate vertices (except starting point AA)
zero_flow_state_vertices.remove(G["AA"])
for vertex in G.values():
    vertex.edges = vertex.edges.difference(zero_flow_state_vertices)
    for zero_v in zero_flow_state_vertices:
        vertex.edge_weights.pop(zero_v, None)

for zero_v in zero_flow_state_vertices:
    G.pop(zero_v.id)

#visualize_graph(G, "input_step3.png")

# Floyd-Warshall all-pairs shortest paths
dist = {u: {v: math.inf for v in G.values()} for u in G.values()}
for u in G.values():
    for v in u.edges:
        dist[u][v] = u.edge_weights[v]
for k in G.values():
    for i in G.values():
        for j in G.values():
            if dist[i][j] > dist[i][k] + dist[k][j]:
                dist[i][j] = dist[i][k] + dist[k][j]


# add those edges -> graph becomes a complete graph
for u in dist:
    for v in dist[u]:
        u.edges.add(v)
        u.edge_weights[v] = dist[u][v]

# remove self-edges, thought I could use them neatly for opening valves (but I didn't)
for u in dist:
    u.edges.remove(u)
    u.edge_weights.pop(u)

#visualize_graph(G, "example_step4.png")


########### ugly area with lots of random heuristic params ###########
# I ended up throwing random heuristics at it to bring down the runtime

# 1: discard neighbors that do not have the max score
# 0.5: only visit neighbors that have at least half of the max neighbor score
# 0: visit all neighbors
#thoroughness = 0.3


thoroughness_offset = 0.45
thoroughness_slope = (0.3-thoroughness_offset)/30
@functools.lru_cache(maxsize=None)
def thoroughness(minutes_left):
    return thoroughness_slope * minutes_left + thoroughness_offset

# cache minute->total_score
best_score_at_minute = {}
# prune if total_score is too low at minutes_left to be probable to be the solution
# much variability allowed at the start, less at the end
score_offset = 0.7
score_slope = (0.5-score_offset)/30
@functools.lru_cache(maxsize=None)
def score_pruning_factor(minutes_left):
    return score_slope * minutes_left + score_offset


# brute-force (with some heuristic)
def run1(valve, total_score, opened, minutes_left):
    global best_score_at_minute
    if len(opened) == len(G) or minutes_left <= 0:
        yield total_score
        return

    if minutes_left in best_score_at_minute:
        if total_score < best_score_at_minute[minutes_left] * score_pruning_factor(minutes_left):
            return
    else:
        best_score_at_minute[minutes_left] = total_score

    # assume that you want to open the valve you are sitting on (if flow_rate>0), which is not always correct
    if valve in opened:  # move to all neighbors
        # calc possible score gain of unvisited neighbors
        neighbors = valve.edges.difference(opened)
        if len(neighbors) == 0 or (minutes_left - 2) <= 0:
            return
        neighbors = [(v, (minutes_left - 2) * v.flow_rate) for v in neighbors]
        #neighbors.sort(key=lambda x: x[1], reverse=True)
        # just assume that lower values won't be correct :^)
        #max_score = neighbors[0][1]
        max_score = max(neighbors, key=lambda a: a[1])[1]
        neighbors = [v for v in neighbors if v[1] >= max_score * thoroughness(minutes_left)]
        for neighbor, _ in neighbors:
            yield from run1(neighbor, total_score, opened, minutes_left - valve.edge_weights[neighbor])
    else:  # open current valve
        opened.add(valve)
        score = (minutes_left - 1) * valve.flow_rate
        yield from run1(valve, total_score + score, opened, minutes_left - 1)
        opened.remove(valve)



# Assume human and elephant won't go to the same valve in the same minute
def run2(valve1, valve2, score1, score2, opened, minutes_left1, minutes_left2):
    if len(opened) == len(G) or (minutes_left1 <= 0 and minutes_left2 <= 0):
        yield score1 + score2
        return

    if minutes_left1 in best_score_at_minute:
        if score1+score2 < best_score_at_minute[minutes_left1] * score_pruning_factor(minutes_left1):
            return
    else:
        best_score_at_minute[minutes_left1] = score1+score2


    # always only do the player-action per function call with the most minutes_left
    if minutes_left1 >= minutes_left2:  # player1
        pass
    else:  # player2
        # do that by switching player1 with player2 variables
        valve1, score1, minutes_left1, valve2, score2, minutes_left2 = valve2, score2, minutes_left2, valve1, score1, minutes_left1

    ####### copy&pasted from part1 ######
    if valve1 in opened:
        # calc possible score gain of unvisited neighbors
        neighbors = valve1.edges.difference(opened)
        if len(neighbors) == 0 or (minutes_left1 - 2) <= 0:
            return
        neighbors = [(v, (minutes_left1 - 2) * v.flow_rate) for v in neighbors]
        # just assume that lower values won't be correct :^)
        #neighbors.sort(key=lambda x: x[1], reverse=True)
        #max_score = neighbors[0][1]
        if 20 <= minutes_left1 <= 30:
            max_score = max(neighbors, key=lambda a: a[1])[1]
            neighbors = [v for v in neighbors if v[1] > max_score * thoroughness(minutes_left1)]
        elif 10 <= minutes_left1 <= 20:
            neighbors = neighbors[:5]  # not correct here, because it's not sorted (but it works)
        else:
            neighbors = neighbors[:2]  # not correct here, because it's not sorted (but it works)
        for neighbor, _ in neighbors:
            yield from run2(neighbor, valve2, score1, score2, opened, minutes_left1 - valve1.edge_weights[neighbor], minutes_left2)
    else:
        opened.add(valve1)
        score = (minutes_left1 - 1) * valve1.flow_rate
        yield from run2(valve1, valve2, score1 + score, score2, opened, minutes_left1 - 1, minutes_left2)
        opened.remove(valve1)



best_score_at_minute = {}
print("silver:", max(run1(G["AA"], 0, {G["AA"]}, 30)))

best_score_at_minute = {}
print("gold:", max(run2(G["AA"], G["AA"], 0, 0, {G["AA"]}, 26, 26)))


