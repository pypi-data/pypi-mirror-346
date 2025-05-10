"""
Módulo para análise de associação de produtos.

Este módulo contém funções para calcular a frequência de produtos,
identificar transações e criar rankings de associações entre produtos.
"""

import pandas as pd
from collections import defaultdict


def calcular_frequencia_produtos(df):
    """
    Calcula a frequência de cada produto no DataFrame.
    
    Args:
        df (pandas.DataFrame): DataFrame com os dados de produtos
        
    Returns:
        pandas.DataFrame: DataFrame com contagem de produtos ordenado por frequência
    """
    # Contar a frequência de cada produto
    contagem_produtos = df['Produto'].value_counts().reset_index()
    contagem_produtos.columns = ['Produto', 'Frequência']
    
    print(f"Total de produtos únicos: {len(contagem_produtos)}")
    print("Top 5 produtos mais frequentes:")
    print(contagem_produtos.head())
    
    return contagem_produtos


def identificar_transacoes(df):
    """
    Identifica transações (pedidos) e separa as que têm múltiplos produtos.
    
    Args:
        df (pandas.DataFrame): DataFrame com os dados de produtos e pedidos
        
    Returns:
        tuple: (todas as transações, transações com múltiplos produtos)
            - todas as transações (pandas.DataFrame): Todas as transações agrupadas por IdPedido
            - transações com múltiplos produtos (pandas.DataFrame): Apenas transações com mais de um produto
    """
    # Agrupar por IdPedido para obter listas de produtos em cada pedido
    transacoes = df.groupby('IdPedido')['Produto'].apply(list).reset_index()
    
    # Adicionar coluna de tamanho para facilitar a filtragem
    transacoes['tamanho'] = transacoes['Produto'].apply(len)
    
    # Filtrar apenas transações com mais de um produto
    transacoes_multiplas = transacoes[transacoes['tamanho'] > 1]
    
    print(f"Total de transações (pedidos): {len(transacoes)}")
    print(f"Transações com múltiplos produtos: {len(transacoes_multiplas)}")
    print(f"Maior número de produtos em uma transação: {transacoes['tamanho'].max()}")
    
    return transacoes, transacoes_multiplas


def criar_ranking_associacoes(transacoes_multiplas, todos_produtos, progress_callback=None):
    """
    Cria um ranking completo de associações entre produtos.
    
    Para cada produto, encontra todos os outros produtos que são comprados junto
    e calcula a frequência dessas associações.
    
    Args:
        transacoes_multiplas (pandas.DataFrame): DataFrame com transações que têm múltiplos produtos
        todos_produtos (pandas.DataFrame): DataFrame com todos os produtos e suas frequências
        progress_callback (callable, opcional): Função para reportar progresso. 
            Deve aceitar dois argumentos: atual e total.
    
    Returns:
        dict: Dicionário onde as chaves são os nomes dos produtos e os valores
            são DataFrames com os produtos associados e suas frequências
    """
    # Dicionário para armazenar associações para cada produto
    associacoes_por_produto = {}
    
    # Lista de todos os produtos únicos
    produtos_unicos = todos_produtos['Produto'].tolist()
    
    print(f"Analisando associações para {len(produtos_unicos)} produtos...")
    
    # Para cada produto, encontrar todos os outros produtos que são comprados junto
    for i, produto_principal in enumerate(produtos_unicos):
        # Mostrar progresso a cada 10 produtos ou usar callback se fornecido
        if progress_callback:
            progress_callback(i+1, len(produtos_unicos))
        elif i % 10 == 0:
            print(f"Processando produto {i+1} de {len(produtos_unicos)}")
        
        # Criar um contador para os produtos associados
        produtos_associados = defaultdict(int)
        
        # Percorrer todas as transações que contêm este produto
        for _, row in transacoes_multiplas.iterrows():
            produtos = row['Produto']
            
            # Se o produto principal está nesta transação
            if produto_principal in produtos:
                # Incrementar o contador para cada outro produto nesta transação
                for outro_produto in produtos:
                    if outro_produto != produto_principal:
                        produtos_associados[outro_produto] += 1
        
        # Converter para DataFrame e ordenar por frequência
        if produtos_associados:
            df_associados = pd.DataFrame([
                (prod, freq) for prod, freq in produtos_associados.items()
            ], columns=['Produto_Associado', 'Frequência'])
            
            df_associados = df_associados.sort_values('Frequência', ascending=False)
            
            # Armazenar no dicionário
            associacoes_por_produto[produto_principal] = df_associados
    
    return associacoes_por_produto