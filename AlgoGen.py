# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 16:25:19 2020

@author: Matheus
"""
#Algoritmo Genético -> knapsack problem 

import numpy as np


class AlgoritmoGenetico():
    '''
    Aplica o algoritimo inteligente em uma função objetivo
    ---------
    Parametros
    ----------
    caso: dict
        Um dicionario com o tipo do item como key.
        Como valor uma tuple (quantidade, peso, valor)
    restricao: int
        Representa o peso limite.
    tam_populacao : int
        O numero de soluções aleatórias geradas.
    num_geracoes : int
        O numero de iteração que ocorrem.
    taxa_mutacao : float, optional
        A probabilidade de ocorrer mutação em um cromossomo.
        O padrão é 0.3.
    '''
    
    def __init__(self, caso, restricao, tam_populacao = 4, num_geracoes = 5, taxa_mutacao = 0.3):
        '''
        Inicializa dos parametros da instância
        '''
        self.quantidade = [i[0] for i in caso.values()]
        self.peso = [i[1] for i in caso.values()]
        self.valor = [i[2] for i in caso.values()]
        self.tam_cromossomo = len(caso)
        self.restricao = restricao
        self.tam_populacao = tam_populacao
        self.taxa_mutacao = taxa_mutacao
        self.num_geracoes = num_geracoes
        
        self._gerar_populacao()
        
    def _ajustar(self, individuo):
        '''
        Verifica se algum cromossomo está fora das restrições e recriar o
        cromossomo neste caso.
        '''
        #Checa as restrições
        if individuo @ self.peso > self.restricao:
            #Gera um novo cromossomo
            individuo = np.asarray([
                np.random.randint(low = 0, high = k+1, size = 1) 
                for k in self.quantidade]).T
            individuo =  individuo[0]
            
            individuo = self._ajustar(individuo)
        #print('ajuste', individuo)
        
        return individuo
    
    def nova_ajuste(self):
        '''
        Ajuste da nova pop
        '''
        for cont_i, i in enumerate(self.populacao):
            self.populacao[cont_i] = self._ajustar(i)
        

    def _gerar_populacao(self):
        '''
        Gera uma população de um determinanado tamanho, com um número 
        de cromossomos de acordo com a função objetivo
        '''
        
        self.populacao = np.asarray([ 
            np.random.randint(low = 0, high = k+1, size = self.tam_populacao) 
            for k in self.quantidade]).T
        
        #Checagem da criacao do indiviuo
        for cont_ind, individuo in enumerate(self.populacao): 
            self.populacao[cont_ind] = self._ajustar(individuo)
        
    def _funcao_objetivo(self, individuo):
        """
            Calcula a função objetivo utilizada para avaliar as soluções.
        """
        return individuo @ self.valor

    def avaliar(self):
        '''
        Avalia as soluções produzidas
        '''
        #Checa o valor
        self.avaliacao = []
        self.soma_avaliacao = 0
        for individuo in self.populacao:
            self.avaliacao.append(self._funcao_objetivo(individuo))
            self.soma_avaliacao += self._funcao_objetivo(individuo)
             
    def selecao(self):

        """
        Realiza a seleção do individuo por torneio.
        """
         #Seleciona duas pontuções (individuos) aleatoriamente
        pontuacao_1 = self.avaliacao[np.random.randint(self.tam_populacao)]
        pontuacao_2 = self.avaliacao[np.random.randint(self.tam_populacao)]
        
        #Realiza o torneio e seleciona a maior pontuacao
        if pontuacao_1 >= pontuacao_2:
            return self.populacao[self.avaliacao.index(pontuacao_1)]
        else:
            return self.populacao[self.avaliacao.index(pontuacao_2)]    

    
    def crossover(self, pai, mae):
        """
        Aplica o crossover.
        """
        #Seleciona dois cromossomos para serem alterados
        cromossomo_1 = np.random.randint(self.tam_cromossomo)
        cromossomo_2 = np.random.randint(self.tam_cromossomo)
        l_crom = [cromossomo_1, cromossomo_2]
        #faz a copia
        filho1 = np.copy(pai)
        filho2 = np.copy(mae)
        #ajusta o cromossomo dos filhos
        for i in l_crom:
            temp = filho1[i]
            filho1[i] = filho2[i]
            filho2[i] = temp
        
        l_filho = [filho1, filho2]
        
        for cont_i, i in  enumerate(l_filho):
            l_filho[cont_i] = self._ajustar(i)
            
        #print(l_filho,'apos_c')
        return filho1, filho2
    
    def mutar(self, filho1, filho2):
        """
        Aplica a mutaçao de acordo com uma probabilidade (taxa de mutação).
        """
        #lista de filho
        lista_filho = [filho1, filho2]
        
        #Seleciona um filho para sofre mutação
        sel_filho = np.random.randint(len(lista_filho))
        
        #Aplica a mutacao de acordo taxa
        if self.taxa_mutacao > np.random.randint(100)/100:
            #Seleciona um cromossomo a ser mutado
            selec_cromossomo = np.random.randint(self.tam_cromossomo)
            
            
            lista_filho[sel_filho][selec_cromossomo] = int(np.random.randint(low = 0,
                                high = self.quantidade[selec_cromossomo] + 1))
            
        for cont_i, i in enumerate(lista_filho):
            lista_filho[cont_i] = self._ajustar(i)
        
        #print(lista_filho, 'apos_m')
        
        return filho1, filho2
    
    
    def mais_apto(self):
        '''
        Busca o melhor individuo
        '''
        #Busca a melhor a avaliacao
        best = max(self.avaliacao)
        best_individuo = self.populacao[self.avaliacao.index(best)]
        
        self.best = best
        self.best_individuo = best_individuo
        
        return best, best_individuo
        
    def nova_geracao(self):
        '''
        Cria a nova geracao
        '''
        nova_populacao = []
        nova_populacao.append(self.best_individuo)
        while len(nova_populacao) < self.tam_populacao:
            #seleciona os pais
            pai = self.selecao()
            mae = self.selecao()
            #Crossover
            filho_1, filho_2 = self.crossover(pai, mae)
            #print(filho_1, filho_2, 'geration_c')
            #Realiza a mutacao
            filho_1, filho_2 = self.mutar(filho_1, filho_2)
            #print(filho_1, filho_2, 'geration_m')
            #Adiciona a lista os filhos
            nova_populacao.append(filho_1)
            nova_populacao.append(filho_2)
            
        
        return nova_populacao

def main():
    '''
    Definição da função que ira rodar o problema da mochila.
    Parametro caso (quantidade, peso, valor)
    '''
    #melhor de todos
    best_all, best_indiv_all = 0, []
    #cria a situação
    caso = {1: (3, 3, 40), 2: (2, 5, 100), 3: (5, 2, 50)}
    #Criar uma instancia  do algoritmo genetico
    algo_genetic = AlgoritmoGenetico(caso, 20, 10, 20, 0.7)
    #Avaliação inicial
    algo_genetic.avaliar()
    #Execeta a funcao por n geracoes
    for i in range(algo_genetic.num_geracoes):
        #print('final\n', algo_genetic.populacao)
        best, best_individuo = algo_genetic.mais_apto()
        #imprime o melhor indiviuo da geracao
        print('O melhor individuo da geraçao {} é o {} com uma'\
              ' pontuacao {}'.format(i, best_individuo, best))
        #Gera nova geracao
        nova_pop = algo_genetic.nova_geracao()
        # substitui a população antiga pela nova e realiza sua avaliação
        algo_genetic.populacao = np.asarray(nova_pop)
        algo_genetic.nova_ajuste()
        algo_genetic.avaliar()
        #print('asda', algo_genetic.populacao)
        if best > best_all:
            best_all = best
            best_indiv_all =  best_individuo
            
    print('O melhor individuo de todos é o {} com uma'\
      ' pontuacao {}'.format( best_indiv_all, best_all))
        
def test_algo():
    #melhor de todos
    best_all, best_indiv_all = 0, []
    #cria a situação
    caso = {1: (3, 3, 40), 2: (2, 5, 100), 3: (5, 2, 50)}
    #Criar uma instancia  do algoritmo genetico
    algo_genetic = AlgoritmoGenetico(caso, 20, 4, 100, 0.7)
    #Avaliação inicial
    algo_genetic.avaliar()
    #Execeta a funcao por n geracoes
    for i in range(algo_genetic.num_geracoes):
        #print('final\n', algo_genetic.populacao)
        best, best_individuo = algo_genetic.mais_apto()
        #imprime o melhor indiviuo da geracao
        #print('O melhor individuo da geraçao {} é o {} com uma'\
        #      ' pontuacao {}'.format(i, best_individuo, best))
        #Gera nova geracao
        nova_pop = algo_genetic.nova_geracao()
        # substitui a população antiga pela nova e realiza sua avaliação
        algo_genetic.populacao = np.asarray(nova_pop)
        algo_genetic.nova_ajuste()
        algo_genetic.avaliar()
        
        if best > best_all:
            best_all = best
            best_indiv_all =  best_individuo
            
    #print('O melhor individuo de todos é o {} com uma'\
    #  ' pontuacao {}'.format( best_indiv_all, best_all))
    msg = 'O algoritmo genetico falhou na situação de gerar uma solucao ótima'\
    ' o valor calculado foi {}'.format(best_all)
    
    assert best_all > 280, msg
    
    
if __name__ == '__main__':
    main()
    test_algo()