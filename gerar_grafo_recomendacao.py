# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 22:18:35 2021

@author: Flauberth
"""

import pandas as pd
base = pd.read_csv('pesquisadores_x_artigos.csv')
del base['Unnamed: 0']

lista = []

for (index, registro) in base.iterrows():
    if index == 0: continue
    registro = registro.dropna() # deletando todos os campos vazios
    registro = pd.DataFrame(registro)

    # pegando o professor
    lista.append("//--Pesquisador--")
    lista.append("match (prof"+str(index)+":Professor {id_curriculo: "+str(index)+"})")
    
    aux = []
    for (idx, valor) in registro.iterrows():
        if valor.values >= 0: # e nota dada é maior que zero
            tipo = idx.split('-')[1] # usado para verificar se é artigo ou projeto de pesquisa
            id_producao = idx.split('-')[0]
            nota = str(valor.values[0])
            """Gerar a linha de comando que procura pelo nó do professor e vincula ele a produção"""
            if tipo == 'ProducaoBibliografica':
                lista.append("match (artigo"+str(id_producao)+":ProducaoBibliografica {id_producao: "+id_producao+"})")#query_artigo = "match (artigo"+str(id_producao)+":ProducaoBibliografica {id_producao: "+id_producao+"}) return artigo"+str(id_producao)
                aux.append("   (prof"+str(index)+")-[:AVALIOU {nota: "+ nota +"}]->(artigo"+str(id_producao)+"),")
            else:
                lista.append("match (projeto"+str(id_producao)+":ProjetoPesquisa {id_projeto_pesquisa: '"+id_producao+"'})")
                aux.append("   (prof"+str(index)+")-[:AVALIOU {nota: "+ nota +"}]->(projeto"+str(id_producao)+"),")

    if len(aux)>0:
        #substituindo a virgula do ultimo registro por ; 
        aux.reverse()
        aux[0] = aux[0].replace(',',';')#substituindo
        aux.reverse()#voltando a lista ao normal
        lista.append("create")
        lista.extend(aux)

    lista.append(" ")

import codecs
#f = open("cypher.txt", "w")

f = codecs.open("cypher_recomendacoes.sql", "w", "utf-8")

#file.close()
for element in lista:
    f.write(element + "\n")

f.close()
