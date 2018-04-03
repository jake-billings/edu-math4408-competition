# thickness.py
#
# Description: In this file, we attempt to develop an algorithm to determine the thickness of an arbitrary graph
#
# See: http://mathworld.wolfram.com/GraphThickness.html
#
# Group:
#  - Jake Billings
#  - Patricia Figueroa
#  - Alex Klein
#
# Class: MATH4408
# Date: 03/15/2018

# import all of the graphs Dr. Gethner gave us to test
from graphs import *

# import math stuff
from math import floor

# import networkx
import networkx as nx

# import planarity testing
from planarity import is_planar


# edge_count_of_complete_graph
#
# returns the number of edges that are in a complete graph on n vertices
def edge_count_of_complete_graph(n):
    return n * (n-1) / 2


# thickness()
#
# work-in-progress function
#
# returns an integer representing the thickness of graph g
#  should return the same results as naive_thickness; however, this function contains optimizations for known
#  graph characterizations
#
# tested by test_thickness()
# See: http://mathworld.wolfram.com/GraphThickness.html
def thickness(G):
    # Complete Graphs
    #
    # The thickness of an arbitrary complete graph is given by
    # floor((n+7)/6) (except for where n=9,10 where thickness is 3)
    #
    # Alekseev, V. B.; Goncakov, V. S.
    # https://mathscinet.ams.org/mathscinet-getitem?mr=0460162
    if G.number_of_edges() == edge_count_of_complete_graph(G.number_of_nodes()):
        if G.number_of_nodes() == 9 or G.number_of_nodes() == 10:
            return 3
        else:
            return int(floor((G.number_of_nodes() + 7) / 6))

    # Planar Graphs
    #
    # The thickness of any planar graph is 1
    if is_planar(G):
        return 1

    # All other graphs
    #
    # since we couldn't find a characterization that helps with this graph, we check using
    # Alex's brute-force search algorithm
    return naive_thickness(G)


# naive_thickness()
#
# Alex's algorithm to return the thickness of a graph via
#  brute-force search
#
# returns an integer representing the thickness of graph g
#  however, it may not do so efficiently; use thickness() to receive all optimizations from this library
#
# tested by test_naive_thickness()
# See: http://mathworld.wolfram.com/GraphThickness.html
def naive_thickness(g):
    vs = set()
    gs = [nx.Graph()]
    for e in g.edges():
        vs.add(e[0])
        vs.add(e[1])
        added = False
        for current in gs:
            current.add_edge(e[0], e[1])
            if is_planar(current):
                added = True
                break
            else:
                current.remove_edge(e[0], e[1])

        if not added:
            ng = nx.Graph()
            ng.add_edge(e[0], e[1])
            gs.append(ng)
    for g in gs:
        for v in vs:
            g.add_node(v)
    return len(gs)


def round_robin_thickness(g):
    naive_best = naive_thickness(g)
    if naive_best == 1:
        return 1

    gs = [nx.Graph() for _ in range(naive_best - 1)]
    gedges = [e for e in g.edges()]
    gedges.sort()

    vs = set()
    for e in g.edges():
        vs.add(e[0])
        vs.add(e[1])

    for v in vs:
        for cur in gs:
            cur.add_node(v)

    not_added = []
    for i, edge in enumerate(gedges):
        gi = i % len(gs)
        gs[gi].add_edge(edge[0], edge[1])
        if not is_planar(gs[gi]):
            not_added.append(edge)
            gs[gi].remove_edge(edge[0], edge[1])

    not_added_again = []
    for e in not_added:
        added = False
        for gcur in gs:
            gcur.add_edge(e[0], e[1])
            if is_planar(gcur):
                added = True
                break
            else:
                gcur.remove_edge(e[0], e[1])

        if not added:
            not_added_again.append(e)

    if len(not_added_again) > 0:
        return naive_best

    return len(gs)

# _from_edge_list()
#
# utility function to convert edge lists to networkx graphs
#
# edges: array of tuples representing edges
def _from_edge_list(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    return G


# test_naive_thickness()
#
# unit testing for the function naive_thickness()
def test_naive_thickness():
    print 'test_naive_thickness()'
    print '\tK5 should have thickness 2...'
    assert naive_thickness(_from_edge_list(edgesOfK5)) == 2
    print '\tPassed.'

    print '\tK8 should have thickness 2...'
    assert naive_thickness(_from_edge_list(edgesOfK8)) == 2
    print '\tPassed.'

    print '\tK9 should have thickness 3...'
    assert naive_thickness(_from_edge_list(edgesOfK9)) == 3
    print '\tPassed.'

    print '\tK5 minus one edge should have thickness 1...'
    assert naive_thickness(_from_edge_list(edgesOfK5[:-1])) == 1
    print '\tPassed.'


# test_thickness()
#
# unit testing for the function thickness()
def test_thickness():
    print 'test_thickness()'
    print '\tK5 should have thickness 2...'
    assert thickness(_from_edge_list(edgesOfK5)) == 2
    print '\tPassed.'

    print '\tK8 should have thickness 2...'
    assert thickness(_from_edge_list(edgesOfK8)) == 2
    print '\tPassed.'

    print '\tK9 should have thickness 3...'
    assert thickness(_from_edge_list(edgesOfK9)) == 3
    print '\tPassed.'

    print '\tK5 minus one edge should have thickness 1...'
    assert thickness(_from_edge_list(edgesOfK5[:-1])) == 1
    print '\tPassed.'


# test()
#
# unit testing for graph thickness functions
def test():
    print '----Unit Testing----'
    test_thickness()
    test_naive_thickness()
    print 'Passed all unit tests.'
    print '--End Unit Testing--'


# if anybody ever bothers running this file, run the test function
# then, output the thickness of all of the graphs Dr. Gethner gave us
if __name__ == '__main__':
    # run unit tests
    test()

    # allGraphs is an array of tuples
    #  where the first element is the name of the edge set
    #  and the second element is the edge set itself
    for g in allGraphs:
        print 'Calculating thickness of ' + g[0] + '...'
        print 'Result: ' + str(thickness(_from_edge_list(g[1])))
