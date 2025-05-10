"""
Product Association Analysis

Uma ferramenta para análise de associação de produtos a partir de dados de transações.
"""

__version__ = "0.1.0"

from product_association.data_loader import carregar_dados
from product_association.association_analysis import (
    calcular_frequencia_produtos,
    identificar_transacoes,
    criar_ranking_associacoes
)
from product_association.report_generator import criar_excel_detalhado

__all__ = [
    'carregar_dados',
    'calcular_frequencia_produtos',
    'identificar_transacoes',
    'criar_ranking_associacoes',
    'criar_excel_detalhado'
]