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

from stolen import algorithm_u


# edge_count_of_complete_graph
#
# returns the number of edges that are in a complete graph on n vertices
def edge_count_of_complete_graph(n):
    return n * (n - 1) / 2


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

    # Small Graphs
    #
    # If a graph is pretty small, we can run a brute-force-search
    if G.number_of_edges() < 29:
        return brute_force_thickness(G)

    # All other graphs
    #
    # since we couldn't find a characterization that helps with this graph, we check using
    # Alex's heuristic algorithms
    #
    # note: this is not guaranteed to yield the actual thickness; only a number greater than or equal to it
    return best_thickness(G)


# naive_thickness()
#
# Alex's algorithm to return the thickness of a graph via
#  brute-force-like search
#
# returns an integer that is greater than or equal to the thickness of graph g
#  however, it may not do so efficiently; use thickness() to receive all optimizations from this library
#
# tested by test_naive_thickness()
# See: http://mathworld.wolfram.com/GraphThickness.html
def naive_thickness(g):
    return len(naive_thickness_graphs(g))


def naive_thickness_graphs(g):
    """
    Generate the thickness graphs themselves
    :param g:
    :return:
    """
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
    return gs


def round_robin_thickness(g):
    return len(round_robin_thickness_graphs(g))


def round_robin_thickness_graphs(g):
    """
    Generate round robin thickness graphs
    Take best known solution (naive)
    Allocate n-1 graphs (if > 1 in naive solution)
    Sort Edges
    Round robin edge assignment
    (i.e. try to spread out the edges for each node across the graphs)
    :param g:
    :return:
    """
    naive_best = naive_thickness_graphs(g)
    if len(naive_best) == 1:
        return naive_best

    gs = [nx.Graph() for _ in range(len(naive_best) - 1)]
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

    return gs


def compress_decompositions(decomps):
    """

    :param decomps: nx.Graph[]
    :return: nx.Graph[]
    """
    if len(decomps) < 3:
        # Can't compress 1, and should be 1 if it's 2 but could have been 1
        return decomps
    new_decomps = [nx.Graph() for _ in range(len(decomps) - 1)]
    min_decomp = decomps[-1]

    # Add all last graph edges to new first decomp
    for e in min_decomp.edges():
        new_decomps[0].add_edge(e[0], e[1])

    notAdded = []
    for i, decomp in enumerate(decomps[:-1]):
        for e in decomp.edges():
            new_decomps[i].add_edge(e[0], e[1])
            if not is_planar(new_decomps[i]):
                new_decomps[i].remove_edge(e[0], e[1])
                notAdded.append(e)

    for e in notAdded:
        added = False
        for g in new_decomps[1:]:
            g.add_edge(e[0], e[1])
            if not is_planar(g):
                g.remove_edge(e[0], e[1])
            else:
                added = True
                break

        if not added:
            return decomps

    return compress_decompositions(new_decomps)


def add_all_vertices(g, vs):
    for v in vs:
        g.add_node(v)


def add_edge(g, e):
    g.add_edge(e[0], e[1])
    if is_planar(g):
        return True
    g.remove_edge(e[0], e[1])
    return False


def connect_vertex(g, e):
    if nx.has_path(g, e[0], e[1]):
        return False
    return add_edge(g, e)


def make_tree(g, es):
    not_added = []
    for e in es:
        if not connect_vertex(g, e):
            not_added.append(e)

    return not_added


def connect_length(g, es, l=2):
    if len(es) == 0:
        return []

    added = []
    max_len = 0
    for e in es:
        sp = len(nx.shortest_path(g, e[0], e[1]))
        max_len = max(max_len, sp)
        if len(nx.shortest_path(g, e[0], e[1])) == l:
            if add_edge(g, e):
                added.append(e)

    if len(added) > 0:
        # Edges have been added, so lengths have changed, try adding at min length again
        not_added = [e for e in es if e not in added]
        if len(not_added) == 0:
            return []
        return connect_length(g, not_added, 2)
    elif max_len > l:
        # No additions at this length, but longer paths exist
        return connect_length(g, es, l + 1)
    else:
        return es


def tree_thickness_graphs(g):
    # Create tree before adding any other edges, then add by path length
    gs = []
    vs = set()
    for v in g:
        vs.add(v)
    es = [e for e in g.edges()]

    while len(es) > 0:
        current = nx.Graph()
        add_all_vertices(current, vs)
        es = make_tree(current, es)
        es = connect_length(current, es, 2)
        gs.append(current)

    return gs


def tree_thickness(g):
    return len(tree_thickness_graphs(g))


def best_thickness(g):
    """
    Thickness of best implementation so far
    :param g: nx.Graph
    :return: int
    """
    return len(best_thickness_graphs(g))


def best_thickness_graphs(g):
    """
    The best implementation so far, change when we get a better one...
    :param g: nx.Graph
    :return: nx.Graph[]
    """
    naive = compress_decompositions(naive_thickness_graphs(g))
    round_robin = compress_decompositions(round_robin_thickness_graphs(g))
    tree = compress_decompositions(tree_thickness_graphs(g))

    naive_len = len(naive)
    round_robin_len = len(round_robin)
    tree_len = len(tree)

    min_len = min(naive_len, round_robin_len, tree_len)

    if min_len == naive_len:
        return naive
    elif min_len == round_robin_len:
        return round_robin
    elif min_len == tree_len:
        return tree
    else:
        return round_robin


# brute_force_thickness()
#
# returns the thickness of a graph via brute-force search
# this function does not return in a reasonable amount of time for graphs of thickness >8
def brute_force_thickness(g):
    smallest_thickness = 500
    for thickness_guess in range(2, 4):
        for edge_arrangement in algorithm_u(g.edges(), thickness_guess):
            all_planar = True
            for layer in edge_arrangement:
                if not is_planar(_from_edge_list(layer)):
                    all_planar = False
                    break
            if all_planar and len(edge_arrangement) < smallest_thickness:
                smallest_thickness = len(edge_arrangement)
                break
        if smallest_thickness <= thickness_guess:
            break
    return smallest_thickness


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
def test_brute_force_thickness():
    print('test_brute_force_thickness()')
    print('\tK5 should have thickness 2...')
    assert brute_force_thickness(_from_edge_list(edgesOfK5)) == 2
    print('\tPassed.')

    print('\tK8 should have thickness 2...')
    assert brute_force_thickness(_from_edge_list(edgesOfK8)) == 2
    print('\tPassed.')


# test_naive_thickness()
#
# unit testing for the function naive_thickness()
def test_naive_thickness():
    print('test_naive_thickness()')
    print('\tK5 should have thickness 2...')
    assert naive_thickness(_from_edge_list(edgesOfK5)) == 2
    print('\tPassed.')

    print('\tK8 should have thickness 2...')
    assert naive_thickness(_from_edge_list(edgesOfK8)) == 2
    print('\tPassed.')

    print('\tK9 should have thickness 3...')
    assert naive_thickness(_from_edge_list(edgesOfK9)) == 3
    print('\tPassed.')

    print('\tK5 minus one edge should have thickness 1...')
    assert naive_thickness(_from_edge_list(edgesOfK5[:-1])) == 1
    print('\tPassed.')


# test_thickness()
#
# unit testing for the function thickness()
def test_thickness():
    print('test_thickness()')
    print('\tK5 should have thickness 2...')
    assert thickness(_from_edge_list(edgesOfK5)) == 2
    print('\tPassed.')

    print('\tK8 should have thickness 2...')
    assert thickness(_from_edge_list(edgesOfK8)) == 2
    print('\tPassed.')

    print('\tK9 should have thickness 3...')
    assert thickness(_from_edge_list(edgesOfK9)) == 3
    print('\tPassed.')

    print('\tK5 minus one edge should have thickness 1...')
    assert thickness(_from_edge_list(edgesOfK5[:-1])) == 1
    print('\tPassed.')


# test_isomorphic()
#
# Test that the best implementation generates sets of graphs that are isomorphic to the original
def test_isomorphic():
    print('test_isomorphic()')
    for k, g in allGraphs:
        g = _from_edge_list(g)
        results = best_thickness_graphs(g)
        current = nx.Graph()
        for result in results:
            for e in result.edges():
                current.add_edge(e[0], e[1])

        print('{} decomposition union is isomorphic to its source graph...'.format(k))
        assert nx.is_isomorphic(g, current)
        print('Passed')


# test()
#
# unit testing for graph thickness functions
def test():
    print('----Unit Testing----')
    test_thickness()
    test_naive_thickness()
    test_brute_force_thickness()
    test_isomorphic()
    print('Passed all unit tests.')
    print('--End Unit Testing--')


# if anybody ever bothers running this file, run the test function
# then, output the thickness of all of the graphs Dr. Gethner gave us
if __name__ == '__main__':
    # run unit tests
    test()

    # allGraphs is an array of tuples
    #  where the first element is the name of the edge set
    #  and the second element is the edge set itself
    for g in allGraphs:
        print('Calculating thickness of ' + g[0] + ' (e=' + str(len(g[1])) + ')...')
        print('Result: ' + str(thickness(_from_edge_list(g[1]))))
