from collections import defaultdict
from copy import deepcopy
from typing import List, Tuple


class Fila:
    def __init__(self):
        self.items = []

    def vazia(self):
        return len(self.items) == 0

    def inserir(self, item):
        self.items.insert(0, item)

    def tirar(self):
        return self.items.pop()

    def tamanho(self):
        return len(self.items)


class Grafo(object):
    qtt_arestas: int
    qtt_vertices: int
    direcionado: bool

    def __init__(self, arestas: List[Tuple[Tuple, int]] = [], lista_adj=defaultdict(set), direcionado=False):
        self.lista_adjacencias = lista_adj
        self.direcionado = direcionado

        if arestas:
            self.adiciona_arestas(arestas)

        self.qtt_arestas = int(len(self.get_arestas()) / 2) if not direcionado else len(self.get_arestas())
        self.qtt_vertices = len(self.get_vertices())

    def get_vertices(self):
        return list(self.lista_adjacencias.keys())

    def get_arestas(self):
        return [(k, v) for k in self.lista_adjacencias.keys() for v in self.lista_adjacencias[k]]

    def adiciona_arestas(self, arestas):
        for u, v in arestas:
            self.adiciona_aresta(u, v)

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

    def adiciona_aresta(self, u, v):
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

    def floresta_melhorado(self):
        visitados = set()

        def busca_em_profundidade(vertice, anterior):
            if vertice in visitados:
                return False

            visitados.add(vertice)

            for adj in self.lista_adjacencias[vertice]:
                if adj != anterior:
                    if not busca_em_profundidade(adj, vertice):
                        return False

            return True

        for vertice in self.lista_adjacencias:
            if vertice not in visitados and not busca_em_profundidade(vertice, -1):
                return False
        return True

    def floresta(self):
        vertices = self.get_vertices()
        visitado = {}
        anterior = {}

        if self.qtt_arestas >= self.qtt_vertices:
            return False

        for vertice in vertices:
            visitado[vertice] = False
            anterior[vertice] = -1

        f = Fila()

        for vertice in vertices:
            if all(visitado.values()):
                break

            visitado[vertice] = True
            f.inserir(vertice)

            while not f.vazia():
                u = f.tirar()

                for w in self.lista_adjacencias[u]:
                    if anterior[u] != w:
                        if not visitado[w]:
                            visitado[w] = True
                            anterior[w] = u
                            f.inserir(w)
                        else:
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

    def arvore_geradora(self, pesos_arestas):
        arestas_floresta = []

        ordenacao = lambda peso: peso[1]
        pesos_arestas.sort(key=ordenacao)

        i = 0
        custo = 0
        while len(arestas_floresta) < self.qtt_vertices - 1:
            arestas_atuais = [pesos_arestas[i][0]]
            arestas_atuais.extend(arestas_floresta)

            if Grafo(arestas=arestas_atuais).floresta_melhorado():
                arestas_floresta.append(pesos_arestas[i][0])
                custo += pesos_arestas[i][1]

            i += 1

        return arestas_floresta, custo


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

    floresta = {
        "1": ["2", "3", "4"],
        "2": ["1"],
        "3": ["1"],
        "4": ["1"],
        "5": ["6"],
        "6": ["5", "7", "8"],
        "7": ["6"],
        "8": ["6"]
    }

    nao_floresta = {
        "1": ["2", "3", "4"],
        "2": ["1"],
        "3": ["1"],
        "4": ["1"],
        "5": ["6", "8"],
        "6": ["5", "7", "8"],
        "7": ["6"],
        "8": ["5", "6"]
    }

    arvore_geradora = ({
        "1": ["2", "3", "4"],
        "2": ["1", "3", "4"],
        "3": ["1", "2", "4", "6"],
        "4": ["1", "2", "3", "5"],
        "5": ["4", "6", "7", "8"],
        "6": ["3", "5", "7", "8"],
        "7": ["5", "6", "8"],
        "8": ["5", "6", "7"]
    },
    [
        (("1", "2"), 6),
        (("1", "3"), 8),
        (("1", "4"), 4),
        (("2", "3"), 1),
        (("2", "4"), 10),
        (("3", "4"), 5),
        (("3", "6"), 3),
        (("4", "5"), 11),
        (("5", "6"), 12),
        (("5", "7"), 9),
        (("5", "8"), 7),
        (("6", "7"), 14),
        (("6", "8"), 13),
        (("7", "8"), 2),
    ])

    grafo_aresta_conexo = Grafo(lista_adj=aresta_conexo)
    print(grafo_aresta_conexo)

    print(f"{2}-Aresta-Conexo? {'Sim' if grafo_aresta_conexo.aresta_conexo(grafo_aresta_conexo, 2) else 'Não'}")
    print(f"{3}-Aresta-Conexo? {'Sim' if grafo_aresta_conexo.aresta_conexo(grafo_aresta_conexo, 3) else 'Não'}")

    grafo_vertice_conexo = Grafo(lista_adj=vertice_conexo)
    print(grafo_vertice_conexo)
    print(f"{1}-Vertice-Conexo? {'Sim' if grafo_vertice_conexo.vertice_conexo(grafo_vertice_conexo, 1) else 'Não'}")
    print(f"{2}-Vertice-Conexo? {'Sim' if grafo_vertice_conexo.vertice_conexo(grafo_vertice_conexo, 2) else 'Não'}")
    print(f"{3}-Vertice-Conexo? {'Sim' if grafo_vertice_conexo.vertice_conexo(grafo_vertice_conexo, 3) else 'Não'}")

    grafo_floresta = Grafo(lista_adj=floresta)
    print(grafo_floresta)
    print(f"Floresta? {'Sim' if grafo_floresta.floresta() else 'Não'}")
    print(f"Conexo? {'Sim' if grafo_floresta.conexo() else 'Não'}")

    grafo_nao_floresta = Grafo(lista_adj=nao_floresta)
    print(nao_floresta)
    print(f"Floresta? {'Sim' if grafo_nao_floresta.floresta() else 'Não'}")
    print(f"Conexo? {'Sim' if grafo_nao_floresta.conexo() else 'Não'}")

    # grafo_arvore_geradora = Grafo(lista_adj=arvore_geradora[0])
    # print(grafo_arvore_geradora.arvore_geradora(arvore_geradora[1]))

    # teste2 = [('1', '4'), ('3', '4'), ('2', '3'), ('5', '8'), ('7', '8'), ('3', '6')]
    # gra = Grafo(arestas=teste2)
    # print(gra.floresta_melhorado())

