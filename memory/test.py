from base import *
import matplotlib.pyplot as plt
import pytest

bm = BaseMemory()
n1 = bm.match_node(1)
n2 = bm.match_node(2, num=True)
n3 = bm.match_node(3, num=True)
n4 = bm.match_node(4)
e1 = bm.match_edge(n1, n2, 1)
e2 = bm.match_edge(n1, n3, 2)
e3 = bm.match_edge(n1, n4, 3)


def test_incident_edges():
    edges = bm.incident_edges(n1)
    assert edges == [e1, e2, e3]
    edges = bm.incident_edges(n1, num_eq=True)
    assert edges == [e1, e2]


def test_incident_nodes():
    nodes = bm.incident_nodes(n1)
    assert nodes == [n2, n3, n4]
    nodes2 = bm.incident_nodes(n1, num_eq=True)
    assert nodes2 == [n2, n3]


def test_sort():
    edges = bm.sort_weight_edges(n1, n=1, num_eq=True)
    assert edges[0]['weight'] == 2


def plot():
    bm = BaseMemory()
    n1 = bm.match_node(1)
    n2 = bm.match_node(2)
    n3 = bm.match_node(3)
    n4 = bm.match_node(4)
    n5 = bm.match_node(5)
    bm.match_edge(n1, n2, 1)
    bm.match_edge(n1, n3, 2)
    bm.match_edge(n1, n4, 3)

    bm.plot()

    # data = bm.data
    # fig, ax = plt.subplots(figsize=(10, 10))
    # layout = data.layout("auto")
    # ig.plot(data,
    #         target=ax,
    #         layout=layout,
    #         vertex_label=data.vs["name"],
    #         vertex_size=50)

    # plt.show()


if __name__ == "__main__":
    pytest.main([__file__])
    #plot()
