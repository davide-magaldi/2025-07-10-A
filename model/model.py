import copy

from database.DAO import DAO
import networkx as nx


class Model:

    def __init__(self):
        self.graph = nx.DiGraph()
        self.idMap = {}
        self.bestSol = []
        self.bestScore = 0
        self.max_weight = 0

    def buildGraph(self, cat, first, last):
        self.graph.clear()
        nodes = DAO.getNodes(cat)
        self.graph.add_nodes_from(nodes)
        for n in nodes:
            self.idMap[n.product_id] = n
        edges = DAO.getEdges(cat, first, last)
        self.max_weight = edges[0][2]
        for e in edges:
            self.graph.add_edge(self.idMap[e[0]], self.idMap[e[1]], weight=e[2])

    def getInfoGraph(self):
        return self.graph.number_of_nodes(), self.graph.number_of_edges()

    def getBestProducts(self):
        nodes = list(self.graph.nodes)
        products = {}
        for n in nodes:
            res = 0
            usc = 0
            ent = 0
            succ = self.graph.successors(n)
            for s in succ:
                usc += self.graph.get_edge_data(n, s)['weight']
            prec = self.graph.predecessors(n)
            for p in prec:
                ent += self.graph.get_edge_data(p, n)['weight']
            res = usc-ent
            products[n] = res
        items = products.items()
        diz = sorted(items, key=lambda i: i[1], reverse=True)
        return diz[:5]

    def getBestPath(self, lun, start, end):
        self.bestScore = 0
        self.bestSol = []
        parziale = [start]
        self.findNext(parziale, lun, end)
        return self.bestSol, self.bestScore

    def findNext(self, parziale, lun, end):
        if len(parziale) == lun:
            if parziale[-1] == end:
                score = self.getScore(parziale)
                if score > self.bestScore:
                    self.bestSol = copy.deepcopy(parziale)
                    self.bestScore = score
            return

        if end in parziale[:lun-1]:
            return

        if self.getScore(parziale) + self.max_weight * (lun - len(parziale)) <= self.bestScore:
            return

        for s in self.graph.successors(parziale[-1]):
            if s not in parziale:
                parziale.append(s)
                self.findNext(parziale, lun, end)
                parziale.pop()

    def getScore(self, sol):
        score = 0
        for i in range(len(sol)-1):
            score += self.graph.get_edge_data(sol[i], sol[i+1])['weight']
        return score




    def getDateRange(self):
        return DAO.getDateRange()

    def getCategories(self):
        return DAO.getCategories()
