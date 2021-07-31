# -*- coding: utf-8 -*-
"""
Created on Sun Jun  6 10:22:06 2021

@author: Flauberth
"""

# Criar registro numa tabela
# Create (p:Person {name: 'John Doe'}) RETURN p

import os
import psycopg2

con = psycopg2.connect(
    host=os.environ.get('host'), database=os.environ.get('database'),
    user=os.environ.get('user'), password=os.environ.get('password')
)
   
cur = con.cursor()


# Buscando todos os pesquisadores
sql = "select id_curriculo, nome_completo, uf_nascimento, categoria   from curriculo order by nome_completo"
cur.execute(sql)
professores = cur.fetchall()
professores = list([{"id": "pesquisador"+str(p[0]), "nome": p[1], "uf": p[2], "categoria": p[3]} for p in professores])

#Criando os nós de Pesquisadores
lista = []
for professor in professores:
    # buscando todas as producoes bibliográficas do professor atual
    lista.append(f"//--Pesquisador: {professor['nome']}")
    lista.append("CREATE ("+professor['id']+":Professor {nome:'"+professor['nome']+"', uf: '"+professor['uf']+"', categoria: '"+professor['categoria']+"'"+ ", id_curriculo: "+professor['id'].replace('pesquisador','')+"})")

    sql = f"""
    select id_producao, titulo_producao, ano_producao, tipo_producao, natureza from producaobibliografica as p
    join curriculo as c on c.id_curriculo=p.id_curriculo_id
    where nome_completo='{professor['nome']}' and tipo_producao='1'
    """
    cur.execute(sql)
    producoes_bibliograficas = cur.fetchall()

    # Se encontrou artigos para esse professor...
    if producoes_bibliograficas:
        producoes_bibliograficas = list([{"id": "producao"+str(p[0]), "titulo": p[1].replace("'",''), "ano": p[2], "tipo": p[3], 'natureza': p[4]} for p in producoes_bibliograficas])

        #lista.append("// Produções bibliográficas")
        for producao in producoes_bibliograficas:
            lista.append("CREATE ("+producao['id']+":ProducaoBibliografica {titulo: '"+producao['titulo']+"', ano: "+producao['ano']+", tipo : '"+producao['tipo']+"', natureza: '"+producao['natureza']+"'"+", id_producao: "+producao['id'].replace('producao','')+"})")
            lista.append("CREATE ("+professor['id']+")-[:PUBLICOU]->("+producao['id']+")") # (id_professor)-[:PRODUZIU]->(id_producao)
            lista.append(" ")

    # Pegando projetos de pesquisa
    sql = f"""
    select id_projeto_pesquisa, nome_projeto, descricao_projeto, data_inicio from projetos_pesquisa as p
    join curriculo as c on c.id_curriculo=p.id_curriculo_id
    where nome_completo='{professor['nome']}'
    """
    cur.execute(sql)
    projetos = cur.fetchall()

    # Se tiver projetos..
    if projetos:
        projetos = list([{"id": "projeto"+str(p[0]), "nome_projeto": p[1].replace("'",''), "descricao_projeto": p[2].replace("'",''), "data_inicio": p[3]} for p in projetos])

        for projeto in projetos:
            lista.append("CREATE ("+projeto['id']+":ProjetoPesquisa {nome_projeto: '"+projeto['nome_projeto']+"', data_inicio : "+projeto['data_inicio']+", id_projeto_pesquisa: '"+projeto['id'].replace('projeto','')+"'})")
            lista.append("CREATE ("+professor['id']+")-[:PROJETOU]->("+projeto['id']+")")
            lista.append(" ")
        


import codecs
#f = open("cypher.txt", "w")

f = codecs.open("cypher.sql", "w", "utf-8")

#file.close()
for element in lista:
    f.write(element + "\n")

f.close()

