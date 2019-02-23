import argparse
import sys
import time
from collections import defaultdict
from functools import wraps

import numpy as np

from math_utils import get_boolean_adjacency_matrices, remove_terminals
from parsing_utils import parse_graph, parse_grammar, products_set
from matmul import update_matrix_cpu, update_matrix_gpu, matrices_from_gpu, matrices_to_gpu


VERBOSE = False


def time_measure(f):
    @wraps(f)
    def inner(*args, **kwargs):
        time_start = time.time()
        out = f(*args, **kwargs)
        time_stop = time.time()
        return out, time_stop - time_start
    return inner


def main(grammar_file, graph_file, args):
    grammar, inverse_grammar = parse_grammar(grammar_file)
    graph, graph_size = parse_graph(graph_file)

    matrices = get_boolean_adjacency_matrices(grammar, inverse_grammar, graph, graph_size)
    remove_terminals(grammar, inverse_grammar)

    # supposing that matrices being altered in-place
    if not args.on_cpu:
        matrices_to_gpu(matrices)

    _, time_elapsed = iterate_on_grammar(grammar, inverse_grammar, matrices)

    if not args.on_cpu:
        matrices_from_gpu(matrices)

    get_solution(matrices, args.output)
    print(int(1000 * (time_elapsed + 0.0005)))


def get_solution(matrices, file=sys.stdout):
    if type(file) is str:
        file = open(file, 'wt')
    else:
        assert file is sys.stdout, f'Only allowed to print solution in file or stdout, not in {file}'
    
    for nonterminal, matrix in matrices.items():
        xs, ys = np.where(matrix)
        # restoring true vertices numbers
        xs += 1
        ys += 1
        pairs = np.vstack((xs, ys)).T
        print(nonterminal, end=' ', file=file)
        print(' '.join(map(lambda pair: ' '.join(pair), pairs.astype('str').tolist())), file=file)


@time_measure
def iterate_on_grammar(grammar, inverse_grammar, matrices):
    inverse_by_nonterm = defaultdict(set)
    for body, heads in inverse_grammar.items():
        assert type(body) is tuple, 'Left terminals in grammar: {}'.format(body)
        for head in heads:
            if body[0] != head:
                inverse_by_nonterm[body[0]].add((head, body))
            if body[1] != head:
                inverse_by_nonterm[body[1]].add((head, body))
    to_recalculate = products_set(grammar)
    while to_recalculate:
        head, body = to_recalculate.pop()
        assert type(body) is tuple, 'Body is either str or tuple, not {}'.format(type(body))
        is_changed = update_matrix(matrices, head, body)
        if not is_changed:
            continue
        for product in inverse_by_nonterm[head]:
            if product != (head, body):
                to_recalculate.add(product)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('grammar', type=str, help='File with grammar in CNF')
    parser.add_argument('graph', type=str, help='Path to a directional graph')
    parser.add_argument('-o', '--output', type=str, help='Path to output file')
    parser.add_argument('-v', '--verbose', action='store_true', help='Print logs into console')
    parser.add_argument('-c', '--on_cpu', action='store_true', help='Naive multiplication on CPU')
    args = parser.parse_args()
    if args.output is None:
        args.output = sys.stdout
    VERBOSE = args.verbose
    update_matrix = update_matrix_cpu if args.on_cpu else update_matrix_gpu

    main(args.grammar, args.graph, args=args)
