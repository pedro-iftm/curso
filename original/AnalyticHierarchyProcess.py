# coding=UTF-8
import numpy as np


class AHP():

    def __init__(self, metodo, precisao, alternativas, criterios, subCriterios, matrizesPreferencias, log=False):
        self.metodo = metodo
        self.precisao = precisao
        self.alternativas = alternativas
        self.criterios = criterios
        self.subCriterios = subCriterios
        self.matrizesPreferencias = matrizesPreferencias
        self.log = log

        self.prioridadesGlobais = []

    @staticmethod
    def Aproximado(matriz, precisao):
        soma_colunas = matriz.sum(axis=0)
        matriz_norm = np.divide(matriz, soma_colunas)
        media_linhas = matriz_norm.mean(axis=1)

        return media_linhas.round(precisao)

    @staticmethod
    def Geometrico(matriz, precisao):
        media_geometrica = [np.prod(linha) ** (1 / len(linha)) for linha in matriz]
        media_geometrica_norm = media_geometrica / sum(media_geometrica)

        return media_geometrica_norm.round(precisao)

    @staticmethod
    def Autovalor(matriz, precisao, interacao=100, autovetor_anterior=None):
        matriz_quadrada = np.linalg.matrix_power(matriz, 2)
        soma_linhas = np.sum(matriz_quadrada, axis=1)
        soma_coluna = np.sum(soma_linhas, axis=0)
        autovetor_atual = np.divide(soma_linhas, soma_coluna)

        if autovetor_anterior is None:
            autovetor_anterior = np.zeros(matriz.shape[0])

        diferenca = np.subtract(autovetor_atual, autovetor_anterior).round(precisao)
        if not np.any(diferenca):
            return autovetor_atual.round(precisao)

        interacao -= 1
        if interacao > 0:
            return AHP.Autovalor(matriz_quadrada, precisao, interacao, autovetor_atual)
        else:
            return autovetor_atual.round(precisao)

    @staticmethod
    def Consistencia(matriz):
        if matriz.shape[0] and matriz.shape[1] > 2:
            # Teorema de Perron-Frobenius
            lambda_max = np.real(np.linalg.eigvals(matriz).max())
            ic = (lambda_max - len(matriz)) / (len(matriz) - 1)
            ri = {3: 0.52, 4: 0.89, 5: 1.11, 6: 1.25, 7: 1.35, 8: 1.40, 9: 1.45,
                  10: 1.49, 11: 1.52, 12: 1.54, 13: 1.56, 14: 1.58, 15: 1.59}
            rc = ic / ri[len(matriz)]
        else:
            lambda_max = 0
            ic = 0
            rc = 0

        return lambda_max, ic, rc

    def VetorPrioridadesLocais(self):
        vetor_prioridades_locais = {}
        for criterio in self.matrizesPreferencias:
            matriz = np.array(self.matrizesPreferencias[criterio])
            if self.metodo == 'aproximado':
                prioridades_locais = self.Aproximado(matriz, self.precisao)
            elif self.metodo == 'geometrico':
                prioridades_locais = self.Geometrico(matriz, self.precisao)
            else:
                if matriz.shape[0] and matriz.shape[1] >= 2:
                    prioridades_locais = self.Autovalor(matriz, self.precisao)
                else:
                    prioridades_locais = self.Aproximado(matriz, self.precisao)

            vetor_prioridades_locais[criterio] = prioridades_locais

            lambda_max, ic, rc = self.Consistencia(matriz)

            if self.log:
                print('\nPrioridades locais do criterio ' + criterio + ':\n', prioridades_locais)
                print('Soma: ', np.round(np.sum(prioridades_locais), self.precisao))
                print('Lambda_max = ', lambda_max)
                print('Indice de Consistencia ' + criterio + ' = ', round(ic, self.precisao))
                print('Razão de Concistência ' + criterio + ' = ', round(rc, 2))

        return vetor_prioridades_locais

    def VetorPrioridadesGlobais(self, prioridades, pesos, criterios):
        for criterio in criterios:
            peso = pesos[criterios.index(criterio)]
            prioridades_locais = prioridades[criterio]
            prioridade_global = np.round(peso * prioridades_locais, self.precisao)

            if criterio in self.subCriterios:
                self.VetorPrioridadesGlobais(prioridades, prioridade_global, self.subCriterios[criterio])
            else:
                self.prioridadesGlobais.append(prioridade_global)

                if self.log:
                    print('\nPrioridades globais do criterio ' + criterio + '\n', prioridade_global)
                    print('Soma: ', sum(prioridade_global).round(self.precisao))

    def Resultado(self):
        prioridades = self.VetorPrioridadesLocais()
        self.VetorPrioridadesGlobais(prioridades, prioridades['criterios'], self.criterios)
        prioridades = np.array(self.prioridadesGlobais)
        prioridades = prioridades.sum(axis=0).round(self.precisao)

        return dict(zip(self.alternativas, prioridades))
