import decompound_annoy
from compound import Compound
from IPython.display import Image
import graphviz as gv

def lattice(c):
    return decompound_annoy.get_decompound_lattice(c, 250, 0.0)

def viterbi(c):
    return decompound_annoy.vit.viterbi_decode(Compound(c, None, lattice(c)))

def draw_lattice(c, l, viterbi=set()):
    a = gv.Digraph()

    a.body.append("subgraph {rank=same; %s }" % (" ".join([ str(key) for key in l ] + [str(len(c))])))

    for (key, v) in l.items():
        for (from_, to, label, _, _) in v:
            style = {}

            if ((from_, to)) in viterbi:
                style = {'color': 'red', 'fontcolor': 'red'}

            a.edge(str(from_), str(to), label, style)

    apply_styles(a, styles)

    a.render("x.png")
    Image(filename='x.png')

styles = {
    'graph': {
        'label': '',
        'rankdir': 'TB',
        'overlap': 'scale',
        'splines': 'true'
    },
    'nodes': {

    },
    'edges': {
        'labeldistance': '10'
    }
}

def apply_styles(graph, styles):
    graph.graph_attr.update(
        ('graph' in styles and styles['graph']) or {}
    )
    graph.node_attr.update(
        ('nodes' in styles and styles['nodes']) or {}
    )
    graph.edge_attr.update(
        ('edges' in styles and styles['edges']) or {}
    )
    return graph

vwl = {0: [(0, 21, 'Volkswirtschaftslehre', 0, 1.0),
  (0, 5, u'Volks', 12, 0.45278138),
  (0, 5, u'Volks', 161, 0.39893898)],
 5: [(5, 21, 'Wirtschaftslehre', 0, 1.0),
  (5, 16, u'Wirtschafts', 155, 0.39184004),
  (5, 16, u'Wirtschafts', 80, 0.38657355)],
 16: [(16, 21, 'Lehre', 0, 1.0)]}

draw_lattice("Volkswirtschaftslehre", vwl, [ (16, 21) ])



