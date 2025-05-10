"""
Módulo para carregamento e preparação de dados de transações.
"""

import pandas as pd


def carregar_dados(arquivo, encoding='utf-8'):
    """
    Carrega e prepara os dados a partir de um arquivo CSV.
    
    Args:
        arquivo (str): Caminho para o arquivo CSV
        encoding (str, opcional): Codificação do arquivo. Padrão é 'utf-8'.
        
    Returns:
        pandas.DataFrame: DataFrame com os dados carregados e preparados
        
    Raises:
        FileNotFoundError: Se o arquivo não for encontrado
        ValueError: Se as colunas esperadas não forem encontradas
    """
    # Carregar o arquivo CSV
    try:
        df = pd.read_csv(arquivo, encoding=encoding)
    except UnicodeDecodeError:
        # Tentar com diferentes codificações se utf-8 falhar
        df = pd.read_csv(arquivo, encoding='latin1')
    
    # Verificar as primeiras linhas para entender a estrutura
    print("Primeiras linhas do arquivo:")
    print(df.head())
    
    # Verificar colunas
    print("Colunas no arquivo:", df.columns.tolist())
    
    # Verificar se as colunas esperadas existem
    colunas_esperadas = ['IdPedido', 'Produto']
    for coluna in colunas_esperadas:
        if coluna not in df.columns:
            print(f"Aviso: Coluna esperada '{coluna}' não encontrada.")
            
            # Tentar identificar colunas similares
            colunas_similares = [col for col in df.columns if coluna.lower() in col.lower()]
            if colunas_similares:
                print(f"Renomeando coluna '{colunas_similares[0]}' para '{coluna}'")
                df = df.rename(columns={colunas_similares[0]: coluna})
            else:
                raise ValueError(f"Coluna '{coluna}' não encontrada e não foi possível identificar uma coluna similar.")
    
    # Limpar valores nulos ou duplicados
    df = df.dropna(subset=['IdPedido', 'Produto'])
    
    # Converter IdPedido para string (para garantir que funcione como identificador)
    df['IdPedido'] = df['IdPedido'].astype(str)
    
    return df