#!/usr/bin/env python3
import sys
from random import shuffle, seed
from typing import TextIO, Optional

from algoritmia.datastructures.graphs import UndirectedGraph
from algoritmia.datastructures.mergefindsets import MergeFindSet
from algoritmia.datastructures.queues import Fifo

Vertex = tuple[int, int]
Edge = tuple[Vertex, Vertex]

NO_VALID_WALL = 'NO VALID WALL'

# Función ya implementada
# Esta función utiliza un MFSet para crear un laberinto, pero le añade n aristas
# adicionales que provocan que el laberinto tenga ciclos.


def create_labyrinth(rows: int, cols: int, n: int, s: int) -> UndirectedGraph[Vertex]:
    vertices: list[Vertex] = [(r, c) for r in range(rows) for c in range(cols)]
    mfs: MergeFindSet[Vertex] = MergeFindSet((v,) for v in vertices)
    edges: list[Edge] = [((r, c), (r + 1, c)) for r in range(rows - 1) for c in range(cols)]
    edges.extend([((r, c), (r, c + 1)) for r in range(rows) for c in range(cols - 1)])
    seed(s)
    shuffle(edges)
    corridors: list[Edge] = []
    for (u, v) in edges:
        if mfs.find(u) != mfs.find(v):
            mfs.merge(u, v)
            corridors.append((u, v))
        elif n > 0:
            n -= 1
            corridors.append((u, v))
    return UndirectedGraph(E=corridors)


def read_data(f: TextIO) -> tuple[UndirectedGraph[Vertex], int, int]:
    rows=int(f.readline())
    cols=int(f.readline())
    n=int(f.readline())
    s=int(f.readline())
    lab=create_labyrinth(rows,cols,n,s)
    return lab,rows,cols


def process(lab: UndirectedGraph[Vertex], rows: int, cols: int) -> tuple[Optional[Edge], int, int]:
    final: Vertex= rows-1,cols-1
    e=bf_search(lab,(0,0),final)
    s=bf_search(lab,final,(0,0))
    len_bf:int= e.get(final)
    fn_len=len_bf
    edge = ((0, 0), (0, 0))
    for r in range(rows):
        for c in range(cols):
            if e.get((r, c)) is not None and s.get((r+1, c)) is not None:
                suma1 = e.get((r, c)) + s.get((r + 1, c)) + 1
                if suma1<fn_len:
                    fn_len = suma1
                    edge = ((r,c),(r+1,c))
            if e.get((r, c)) is not None and s.get((r, c+1)) is not None:
                suma2 = e.get((r, c)) + s.get((r, c + 1)) +1
                if suma2<fn_len:
                    fn_len = suma2
                    edge = ((r,c),(r,c+1))
    if edge == ((0, 0), (0, 0)):
        return None, len_bf, len_bf
    return edge, len_bf, fn_len


def bf_search(graph: UndirectedGraph[Vertex],vIni: Vertex, vFin: Vertex) -> dict[Vertex,int]:
    mapa: dict[Vertex,int] = dict()
    mapa[vIni] = 0
    seen: set[Vertex]=set()
    seen.add(vIni)
    queue: Fifo[Edge]=Fifo()
    queue.push((vIni,vIni))
    while len(queue)>0:
        u,v= queue.pop()
        if v==vFin:
            return mapa
        for suc in graph.succs(v):
            if suc not in seen:
                i = mapa.get(v)+1
                mapa[suc] = i
                queue.push((v, suc))
                seen.add(suc)
    return mapa


def show_results(edge_to_add: Optional[Edge], length_before: int, length_after: int):
    if edge_to_add is None:
        print(NO_VALID_WALL)
    else:
        print(edge_to_add[0][0], edge_to_add[0][1], edge_to_add[1][0], edge_to_add[1][1])
    print(length_before)
    print(length_after)


if __name__ == '__main__':
    graph0, rows0, cols0 = read_data(sys.stdin)
    edge_to_add0, length_before0, length_after0 = process(graph0, rows0, cols0)
    show_results(edge_to_add0, length_before0, length_after0)
