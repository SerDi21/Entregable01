#!/usr/bin/env python3
import sys

from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.viewers.labyrinth_viewer import LabyrinthViewer

from entregable1 import read_data, process, NO_VALID_WALL

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("Ejemplo de uso: entregable_viewer.py pruebas_test/lab_006x008.i")
        sys.exit(1)

    with open(sys.argv[1]) as f:
        graph, rows, cols = read_data(f)

    graph_copy = UndirectedGraph(V=graph.V, E=graph.E)  # Por si el process lo estropea

    edge_to_add, length_before, length_after = process(graph, rows, cols)

    if edge_to_add is None:
        print(f'{NO_VALID_WALL}: THIS INSTANCE HAS NO SOLUTION')
        sys.exit(1)

    lv = LabyrinthViewer(graph_copy,
                         canvas_width=400,
                         canvas_height=400,
                         margin=10,
                         wall_width=4)

    lv.set_input_point((0, 0))
    lv.set_output_point((rows - 1, cols - 1))
    lv.add_marked_cell(edge_to_add[0])
    lv.add_marked_cell(edge_to_add[1])

    lv.run()
