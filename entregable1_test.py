#!/usr/bin/env python3
import sys, io, subprocess
from time import process_time
from traceback import print_tb
from typing import Union, Optional
from contextlib import redirect_stdout

from entregable1 import read_data, process, show_results, Edge, NO_VALID_WALL

def run(cmd: str) -> Union[tuple[list[str], list[str]], str]:
    try:
        res0 = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        err = str(res0.stderr, 'utf-8').strip()
        res = str(res0.stdout, 'utf-8').strip()
        return err.split('\n'), res.split('\n')
    except subprocess.CalledProcessError as e:
        return f"CalledProcessError: Return code = {e.returncode}"
    except Exception as e:
        return f"ERROR: {e}"

def get_lines_and_solution(filename: str) -> tuple[list[str], tuple[Optional[Edge], int, int]]:
    with open(filename) as f:
        sol_lines = [line.strip() for line in f.readlines()]
    if sol_lines[0] == NO_VALID_WALL:
        edge_to_add_sol = None
    else:
        r0, c0, r1, c1 = (int(e) for e in sol_lines[0].split())
        edge_to_add_sol = (r0, c0), (r1, c1)
    length_before_sol = int(sol_lines[1])
    length_after_sol = int(sol_lines[2])

    solution = (edge_to_add_sol, length_before_sol, length_after_sol)
    return sol_lines, solution


def error(message, tb):
    sys.stderr.write(message + "\n")
    print_tb(tb, file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Ejemplo de uso: python3.10 entregable_test.py public_test/lab_008x010.i public_test/lab_008x010.o")
        sys.exit(1)

    sol_lines, solution = get_lines_and_solution(sys.argv[2])

    with open(sys.argv[1]) as f:
        try:
            graph, rows, cols = read_data(f)
        except Exception as e:
            tb = sys.exc_info()[2]
            error(f"ERROR. Tu función 'read_data()' ha lanzado una excepción: {e}", tb)

    try:
        t0 = process_time()
        result = process(graph, rows, cols)
        t1 = process_time()
        elapsed_time = t1 - t0
    except Exception as e:
        tb = sys.exc_info()[2]
        error(f"ERROR. Tu función 'process()' ha lanzado una excepción: {e}", tb)

    try:
        f = io.StringIO()
        with redirect_stdout(f):
            show_results(*result)
        lines = f.getvalue().strip().split('\n')
    except Exception as e:
        tb = sys.exc_info()[2]
        error(f"ERROR. Tu función 'show_results()' ha lanzado una excepción: {e}", tb)

    if result == solution:
        if lines != sol_lines:
            print("ERROR. Tu función 'show_result()' no muestra las líneas que debería:")
            print(f"-------------------- Salida correcta (archivo '{sys.argv[2]}'):")
            for line in sol_lines: print(line)
            print("-------------------- Tu salida:")
            for line in lines: print(line)
            print("--------------------")
            sys.exit(1)

        if elapsed_time < 1:
            print(f"SOLUTION OK - TIME OK ({elapsed_time:.2f} sec)")
        else:
            print(f"SOLUTION OK - TIME ERROR ({elapsed_time:.2f} sec)")
    else:
        # TODO aquí no llega nunca
        if elapsed_time < 1:
            print(f"SOLUTION ERROR - TIME OK ({elapsed_time:.2f} sec)")
        else:
            print(f"SOLUTION ERROR - TIME ERROR ({elapsed_time:.2f} sec)")
        print(' - Expected solution:', solution)
        print(' - Obtained solution:', result)

