import os
import ast

from collections import defaultdict

def find_py_files(root_dir):
    for root, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                yield os.path.join(root, file)

def build_import_graph(root_dir):
    graph = defaultdict(set)
    for filepath in find_py_files(root_dir):
        with open(filepath, 'r', encoding='utf-8') as f:
            node = ast.parse(f.read(), filename=filepath)
        module_name = os.path.splitext(os.path.relpath(filepath, root_dir))[0].replace(os.sep, '.')
        for item in ast.walk(node):
            if isinstance(item, ast.ImportFrom) and item.module:
                graph[module_name].add(item.module)
            elif isinstance(item, ast.Import):
                for alias in item.names:
                    graph[module_name].add(alias.name)
    return graph

def detect_cycles(graph):
    visited = set()
    stack = []

    def visit(node):
        if node in stack:
            cycle_index = stack.index(node)
            return [*stack[cycle_index:], node]
        if node in visited:
            return None
        visited.add(node)
        stack.append(node)
        for neighbor in graph.get(node, []):
            cycle = visit(neighbor)
            if cycle:
                return cycle
        stack.pop()
        return None

    for node in graph:
        cycle = visit(node)
        if cycle:
            return cycle
    return None

if __name__ == "__main__":
    graph = build_import_graph("my_project")
    cycle = detect_cycles(graph)
    if cycle:
        print("Cycle détecté :", " -> ".join(cycle))
    else:
        print("Pas de dépendances circulaires détectées.")
