"""
Interface de linha de comando para a ferramenta de análise de associação de produtos.

Este módulo fornece uma interface de linha de comando para executar a análise
de associação de produtos a partir de um arquivo CSV de transações.
"""

import argparse
import os
import sys
import traceback
from product_association.data_loader import carregar_dados
from product_association.association_analysis import (
    calcular_frequencia_produtos,
    identificar_transacoes,
    criar_ranking_associacoes
)
from product_association.report_generator import criar_excel_detalhado


def main():
    """
    Função principal que processa argumentos da linha de comando e executa o fluxo de análise.
    
    Returns:
        int: 0 para sucesso, 1 para erro
    """
    parser = argparse.ArgumentParser(
        description='Ferramenta para análise de associação de produtos a partir de dados de transações'
    )
    
    parser.add_argument(
        'arquivo_entrada',
        help='Arquivo CSV com dados de transações (obrigatório)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='relatorio_associacoes.xlsx',
        help='Nome do arquivo Excel de saída (padrão: relatorio_associacoes.xlsx)'
    )
    
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='Codificação do arquivo de entrada (padrão: utf-8)'
    )
    
    parser.add_argument(
        '--max-produtos',
        type=int,
        default=20,
        help='Número máximo de produtos para criar abas individuais (padrão: 20)'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Mostrar informações detalhadas durante o processamento'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='%(prog)s 0.1.0',
        help='Mostrar a versão do programa'
    )
    
    args = parser.parse_args()
    
    # Verificar se o arquivo existe
    if not os.path.isfile(args.arquivo_entrada):
        print(f"Erro: Arquivo '{args.arquivo_entrada}' não encontrado.")
        return 1
    
    try:
        # Mostrar mensagem inicial
        if args.verbose:
            print("Iniciando análise de associação de produtos...")
        
        # Carregar dados
        df = carregar_dados(args.arquivo_entrada, encoding=args.encoding)
        if args.verbose:
            print(f"Dados carregados com sucesso. Total de {len(df)} registros.")
        
        # Calcular frequência de produtos
        contagem_produtos = calcular_frequencia_produtos(df)
        if args.verbose:
            print(f"Total de produtos únicos: {len(contagem_produtos)}")
            print("Top 5 produtos mais frequentes:")
            print(contagem_produtos.head())
        
        # Identificar transações
        transacoes, transacoes_multiplas = identificar_transacoes(df)
        if args.verbose:
            print(f"Total de transações (pedidos): {len(transacoes)}")
            print(f"Transações com múltiplos produtos: {len(transacoes_multiplas)}")
            print(f"Maior número de produtos em uma transação: {transacoes['tamanho'].max()}")
        
        # Callback para mostrar progresso
        def progress_callback(atual, total):
            if args.verbose:
                print(f"Processando produto {atual} de {total}")
        
        # Criar ranking de associações
        if args.verbose:
            print("Criando rankings de associações...")
        associacoes_por_produto = criar_ranking_associacoes(
            transacoes_multiplas, 
            contagem_produtos,
            progress_callback if args.verbose else None
        )
        
        # Criar relatório Excel
        if args.verbose:
            print("Gerando relatório Excel...")
        relatorio = criar_excel_detalhado(
            associacoes_por_produto, 
            contagem_produtos, 
            output_file=args.output,
            max_produtos=args.max_produtos
        )
        
        if args.verbose:
            print("\nAnálise concluída com sucesso!")
            print(f"Relatório detalhado criado: {relatorio}")
        else:
            print(f"Relatório criado: {relatorio}")
            
        return 0
            
    except Exception as e:
        print(f"Erro durante a análise: {e}")
        if args.verbose:
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())