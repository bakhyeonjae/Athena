from collections import deque

GRAY, BLACK = 0, 1

class Topology(object):
    def __init__(self):
        self.graph = {}

    def setGraph(self,dag):
        for child in dag.getSrcNodes():
            if child not in self.graph.keys():
                self.graph[child] = []
            self.graph[child].append(dag)
            self.setGraph(child)

    def sort(self):
        order, enter, state = deque(), set(self.graph), {}
        
        def dfs(node):
            state[node] = GRAY
            for k in self.graph.get(node, ()):
                sk = state.get(k, None)
                if sk == GRAY: raise ValueError('cycle')
                if sk == BLACK: continue
                enter.discard(k)
                dfs(k)
            order.appendleft(node)
            state[node] = BLACK

        while enter: dfs(enter.pop())
        return order
