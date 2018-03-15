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
            return floor((G.number_of_nodes() + 7) / 6)

    # Planar Graphs
    #
    # The thickness of any planar graph is 1
    if is_planar(G):
        return 1

    raise NotImplementedError('We don\'t know how to find the thickness of that graph yet')


# _from_edge_list()
#
# utility function to convert edge lists to networkx graphs
#
# edges: array of tuples representing edges
def _from_edge_list(edges):
    G = nx.Graph()
    G.add_edges_from(edges)
    return G


# test_thickness()
#
# unit testing for the function thickness()
def test_thickness():
    print 'K5 should have thickness 2...'
    assert thickness(_from_edge_list(edgesOfK5)) == 2
    print 'Passed.'

    print 'K8 should have thickness 2...'
    assert thickness(_from_edge_list(edgesOfK8)) == 2
    print 'Passed.'

    print 'K9 should have thickness 3...'
    assert thickness(_from_edge_list(edgesOfK9)) == 3
    print 'Passed.'

    print 'K5 minus one edge should have thickness 1...'
    assert thickness(_from_edge_list(edgesOfK5[:-1])) == 1
    print 'Passed.'


# test()
#
# unit testing for graph thickness functions
def test():
    print '----Unit Testing----'
    test_thickness()
    print 'Passed all unit tests.'
    print '--End Unit Testing--'


# if anybody ever bothers running this file, run the test function
if __name__ == '__main__':
    test()
