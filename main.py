from collections import defaultdict
from copy import deepcopy


class Fila:
    def __init__(self):
        self.items = []

    def vazia(self):
        return self.items == []

    def inserir(self, item):
        self.items.insert(0, item)

    def tirar(self):
        return self.items.pop()

    def tamanho(self):
        return len(self.items)


class Grafo(object):
    def __init__(self, arestas=[], lista_adj=defaultdict(set), direcionado=False):
        self.lista_adjacencias = lista_adj
        self.direcionado = direcionado
        if arestas:
            self.adiciona_arestas(arestas)

    def get_vertices(self):
        return list(self.lista_adjacencias.keys())

    def get_arestas(self):
        return [(k, v) for k in self.lista_adjacencias.keys() for v in self.lista_adjacencias[k]]

    def adiciona_arestas(self, arestas):
        for u, v in arestas:
            self.adiciona_arco(u, v)

    def remove_aresta(self, aresta):
        u, v = aresta[0], aresta[1]
        nova_lista = deepcopy(self.lista_adjacencias)
        nova_lista[u].remove(v)
        nova_lista[v].remove(u)
        return Grafo(lista_adj=nova_lista)

    def remove_vertice(self, vertice):
        nova_lista = deepcopy(self.lista_adjacencias)
        nova_lista.pop(vertice)
        nova_lista = {k: list(filter(lambda x: x != vertice, v)) for k, v in nova_lista.items()}
        return Grafo(lista_adj=nova_lista)

    def adiciona_arco(self, u, v):
        self.lista_adjacencias[u].add(v)
        if not self.direcionado:
            self.lista_adjacencias[v].add(u)

    def grau_minimo(self):
        return min([len(i) for i in self.lista_adjacencias.values()])

    def existe_aresta(self, u, v):
        return u in self.lista_adjacencias and v in self.lista_adjacencias[u]

    def __len__(self):
        return len(self.lista_adjacencias)

    def __str__(self):
        return '{}({})'.format(self.__class__.__name__, dict(self.lista_adjacencias))

    def __getitem__(self, v):
        return self.lista_adjacencias[v]

    def completo(self):
        return len(self.get_arestas()) == len(self.get_vertices())**2/2

    def conexo(self):
        visitado = {vertice: False for vertice in self.lista_adjacencias}
        fila = Fila()
        primeiro = list(self.lista_adjacencias.keys())[0]
        fila.inserir(primeiro)
        visitado[primeiro] = True

        while not fila.vazia():
            u = fila.tirar()
            for w in self.lista_adjacencias[u]:
                if not visitado[w]:
                    visitado[w] = True
                    fila.inserir(w)

        return all([i for i in visitado.values()])

    def aresta_conexo(self, g, k):
        if k > g.grau_minimo():
            return False
        if k == 1:
            return g.conexo()

        for aresta in g.get_arestas():
            novo_grafo = g.remove_aresta(aresta)
            if not self.aresta_conexo(novo_grafo, k - 1):
                return False

        return True

    def vertice_conexo(self, g, k):
        if g.completo():
            return True
        if k > g.grau_minimo():
            return False
        if k == 1:
            return g.conexo()
        for vertice in g.get_vertices():
            novo_grafo = g.remove_vertice(vertice)
            if not self.vertice_conexo(novo_grafo, k - 1):
                return False

        return True


if __name__ == '__main__':
    desconexo = {
        "1": ["2", "5", "7"],
        "2": ["1", "3", "5"],
        "3": ["2", "5", "7"],
        "4": ["6", "8", "9"],
        "5": ["1", "2", "3", "7"],
        "6": ["4", "8", "9"],
        "7": ["1", "3", "5"],
        "8": ["4", "6"],
        "9": ["4", "6"]
    }

    conexo = {
        "1": ["2", "5", "7"],
        "2": ["1", "3", "5"],
        "3": ["2", "5", "7"],
        "5": ["1", "2", "3", "7"],
        "7": ["1", "3", "5"],
    }

    aresta_conexo = {
        "1": ["2", "3", "4"],
        "2": ["1", "3", "4"],
        "3": ["1", "2", "4", "5"],
        "4": ["1", "2", "3", "5"],
        "5": ["3", "4", "6", "7", "8"],
        "6": ["5", "7", "8"],
        "7": ["5", "6", "8"],
        "8": ["5", "6", "7"]
    }

    vertice_conexo = {
        "1": ["2", "3", "4"],
        "2": ["1", "3", "4"],
        "3": ["1", "2", "4", "6"],
        "4": ["1", "2", "3", "5"],
        "5": ["4", "6", "7", "8"],
        "6": ["3", "5", "7", "8"],
        "7": ["5", "6", "8"],
        "8": ["5", "6", "7"]
    }

    grafo_aresta_conexo = Grafo(lista_adj=aresta_conexo)
    print(grafo_aresta_conexo)

    print(f"{2}-Aresta-Conexo? {'Sim' if grafo_aresta_conexo.aresta_conexo(grafo_aresta_conexo, 2) else 'Não'}")
    print(f"{3}-Aresta-Conexo? {'Sim' if grafo_aresta_conexo.aresta_conexo(grafo_aresta_conexo, 3) else 'Não'}")

    grafo_vertice_conexo = Grafo(lista_adj=vertice_conexo)
    print(grafo_vertice_conexo)
    print(f"{1}-Vertice-Conexo? {'Sim' if grafo_vertice_conexo.vertice_conexo(grafo_vertice_conexo, 1) else 'Não'}")
    print(f"{2}-Vertice-Conexo? {'Sim' if grafo_vertice_conexo.vertice_conexo(grafo_vertice_conexo, 2) else 'Não'}")
    print(f"{3}-Vertice-Conexo? {'Sim' if grafo_vertice_conexo.vertice_conexo(grafo_vertice_conexo, 3) else 'Não'}")

