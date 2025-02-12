
#include <iostream>
#include "Grammar.h"
#include "Graph.h"
#include "methodOf4RusBooleanSemiringMatrix.h"

int main(int argc, char *argv[]) {
    Grammar grammar = Grammar(argv[1]);
    Graph graph = Graph(argv[2]);
    auto times = grammar.intersection_with_graph<MethodOf4RusMatrix, MethodOf4RusMatricesEnv>(graph);
    std::cout << times.first << ' ' << times.second << std::endl;
    grammar.print_results(argv[3]);
    return 0;
}
