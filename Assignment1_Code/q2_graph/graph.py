"""
graph.py
A generic UNWEIGHTED DIRECTED graph (adjacency-list representation).

Vertices can be ANY hashable Python object (str, int, a Course object, ...).
There is no domain-specific code in this file, so the class is reusable.

For every vertex we keep two lists:
    _out[v] : vertices that v points TO       (v -> w)
    _in[v]  : vertices that point INTO v      (u -> v)
Keeping _in makes listIncomingAdjacentVertex O(deg_in) instead of having to
scan every vertex in the graph (O(V + E)).
"""


class Graph:
    def __init__(self):
        self._out = {}
        self._in = {}

    # ------------------------------------------------------------- vertices
    def addVertex(self, vertex):
        """Add a new vertex. Returns False if it already exists."""
        if vertex in self._out:
            return False
        self._out[vertex] = []
        self._in[vertex] = []
        return True

    def hasVertex(self, vertex):
        return vertex in self._out

    def vertices(self):
        """Return all vertices in insertion order."""
        return list(self._out)

    def removeVertex(self, vertex):
        """Remove a vertex and every edge that touches it."""
        if vertex not in self._out:
            return False
        for target in self._out[vertex]:
            self._in[target].remove(vertex)
        for source in self._in[vertex]:
            self._out[source].remove(vertex)
        del self._out[vertex]
        del self._in[vertex]
        return True

    # ---------------------------------------------------------------- edges
    def addEdge(self, source, target):
        """Add a directed edge source -> target.

        Returns False if either vertex is missing or the edge already exists.
        """
        if source not in self._out or target not in self._out:
            return False
        if target in self._out[source]:
            return False
        self._out[source].append(target)
        self._in[target].append(source)
        return True

    def removeEdge(self, source, target):
        """Remove the edge source -> target. Returns False if it is absent."""
        if source not in self._out or target not in self._out[source]:
            return False
        self._out[source].remove(target)
        self._in[target].remove(source)
        return True

    def hasEdge(self, source, target):
        return source in self._out and target in self._out[source]

    # ------------------------------------------------------------- queries
    def listIncomingAdjacentVertex(self, vertex):
        """List all vertices u that have an edge u -> vertex."""
        if vertex not in self._in:
            return []
        return list(self._in[vertex])

    def listOutgoingAdjacentVertex(self, vertex):
        """List all vertices w that have an edge vertex -> w."""
        if vertex not in self._out:
            return []
        return list(self._out[vertex])

    def hasPath(self, start, goal):
        """True if goal can be reached from start (iterative depth-first search)."""
        if start not in self._out or goal not in self._out:
            return False
        visited, stack = set(), [start]
        while stack:
            v = stack.pop()
            if v == goal:
                return True
            if v in visited:
                continue
            visited.add(v)
            stack.extend(self._out[v])
        return False

    def __len__(self):
        return len(self._out)
