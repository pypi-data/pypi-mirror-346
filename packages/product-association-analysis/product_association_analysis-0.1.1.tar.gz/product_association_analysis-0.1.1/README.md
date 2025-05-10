# 🛒 Product Association Analysis

<div align="center">

  **Descubra quais produtos são frequentemente comprados juntos para impulsionar suas vendas!**
  
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Python 3.6+](https://img.shields.io/badge/Python-3.6+-blue.svg)](https://www.python.org/downloads/)
  [![contributions welcome](https://img.shields.io/badge/contributions-welcome-brightgreen.svg?style=flat)](https://github.com/seu-usuario/product-association-analysis/issues)
  
</div>

---

## 📋 Índice

- [O que é isto?](#-o-que-é-isto)
- [Como isto pode me ajudar?](#-como-isto-pode-me-ajudar)
- [Instalação Passo a Passo](#-instalação-passo-a-passo)
- [Manual Completo](#-manual-completo)
  - [Preparando seus Dados](#preparando-seus-dados)
  - [Executando a Análise](#executando-a-análise)
  - [Entendendo o Relatório](#entendendo-o-relatório)
- [Exemplos de Uso](#-exemplos-de-uso)
- [Solução de Problemas](#-solução-de-problemas)
- [Para Desenvolvedores](#-para-desenvolvedores)
- [Licença](#-licença)
- [Contato e Suporte](#-contato-e-suporte)

---

## 🤔 O que é isto?

**Product Association Analysis** é uma ferramenta que analisa seus dados de vendas para descobrir **quais produtos são frequentemente comprados juntos**. É como ter um analista de dados trabalhando para você, mas totalmente automatizado!

**Exemplo:** Descubra que 75% das pessoas que compram café também compram açúcar, ou que 40% dos clientes que compram um vestido também adquirem um cinto combinando.

---

## 💡 Como isto pode me ajudar?

Esta ferramenta pode **transformar sua estratégia de vendas** com insights poderosos:

### Para equipes de Marketing:
- 📊 Crie promoções mais eficazes combinando produtos relacionados
- 📧 Melhore suas campanhas de email com recomendações personalizadas
- 💰 Aumente o valor médio dos pedidos com sugestões de cross-selling

### Para gestores de Varejo:
- 🏪 Organize sua loja física colocando produtos relacionados próximos
- 🛒 Otimize o layout do seu e-commerce com recomendações automáticas
- 📦 Crie kits e combos baseados em dados reais, não em suposições

### Para equipes de E-commerce:
- 🔍 Melhore seu sistema de "Quem comprou X também comprou Y"
- ⚡ Aumente as taxas de conversão com sugestões relevantes
- 🚀 Impulsione vendas com recomendações baseadas em comportamentos reais

---

## 📥 Instalação Passo a Passo

> **NOTA:** Nunca usou Python antes? Sem problema! Siga exatamente estas instruções e tudo funcionará perfeitamente!

### Windows

1. **Instale o Python**:
   - Baixe o instalador do Python 3.8 ou superior em [python.org](https://www.python.org/downloads/)
   - **IMPORTANTE:** Marque a caixa "Add Python to PATH" durante a instalação
   - Clique em "Install Now"

2. **Instale a ferramenta**:
   - Abra o "Prompt de Comando" (pesquise por "cmd" no menu Iniciar)
   - Cole e execute este comando:
   
   ```bash
   pip install product-association-analysis
   ```

3. **Verifique a instalação**:
   - No mesmo Prompt de Comando, digite:
   
   ```bash
   product-association-analysis --version
   ```
   
   - Você deverá ver a versão do programa, confirmando que está instalado corretamente

### Mac

1. **Instale o Python**:
   - O Mac já vem com Python, mas recomendamos instalar a versão mais recente
   - Baixe o instalador do Python 3.8 ou superior em [python.org](https://www.python.org/downloads/)
   - Abra o arquivo baixado e siga as instruções de instalação

2. **Instale a ferramenta**:
   - Abra o Terminal (pesquise por "Terminal" no Spotlight)
   - Cole e execute este comando:
   
   ```bash
   pip3 install product-association-analysis
   ```

3. **Verifique a instalação**:
   - No mesmo Terminal, digite:
   
   ```bash
   product-association-analysis --version
   ```
   
   - Você deverá ver a versão do programa, confirmando que está instalado corretamente

---

## 📖 Manual Completo

### Preparando seus Dados

A ferramenta funciona melhor com um arquivo CSV contendo seus dados de transações. Se você não sabe o que é um arquivo CSV, pense nele como uma planilha simples que pode ser criada no Excel.

**Formato do arquivo**:
1. Seu arquivo deve ter pelo menos estas duas colunas:
   - `IdPedido`: Um número ou código que identifica cada pedido
   - `Produto`: O nome ou código do produto comprado

2. **Exemplo de como seus dados devem parecer**:

   | IdPedido | Produto         | Quantidade | Valor   |
   |----------|-----------------|------------|---------|
   | 1001     | Camiseta Branca | 2          | 59.90   |
   | 1001     | Calça Jeans     | 1          | 129.90  |
   | 1002     | Tênis Esportivo | 1          | 199.90  |
   | 1003     | Camiseta Branca | 1          | 59.90   |
   | 1003     | Meias           | 3          | 19.90   |

   > **Observação**: As colunas `Quantidade` e `Valor` são opcionais, mas podem ser úteis para análises futuras.

3. **Como exportar do seu sistema**:
   - **Excel/Google Sheets**: Salve como CSV (Arquivo > Salvar como > CSV)
   - **Sistema de vendas**: Procure pela opção "Exportar transações" ou "Relatório de vendas"
   - **E-commerce**: A maioria das plataformas permite exportar pedidos como CSV

### Executando a Análise

Depois de ter seu arquivo CSV pronto, é hora de executar a análise:

1. **Abra o terminal ou prompt de comando**:
   - **Windows**: Aperte a tecla Windows + R, digite `cmd` e pressione Enter
   - **Mac**: Abra o Spotlight (Command + Espaço) e digite `Terminal`

2. **Execute o comando básico**:
   ```bash
   product-association-analysis caminho/para/seu_arquivo.csv
   ```
   
   Substitua `caminho/para/seu_arquivo.csv` pelo caminho real do seu arquivo.
   
   **Exemplo no Windows**:
   ```bash
   product-association-analysis C:\Users\SeuNome\Downloads\vendas.csv
   ```
   
   **Exemplo no Mac**:
   ```bash
   product-association-analysis /Users/SeuNome/Downloads/vendas.csv
   ```

3. **Opções avançadas** (todas opcionais):
   ```bash
   product-association-analysis seu_arquivo.csv --output relatorio_personalizado.xlsx --max-produtos 30 --encoding latin1 --verbose
   ```
   
   - `--output`: Define o nome do arquivo Excel de saída (padrão: relatorio_associacoes.xlsx)
   - `--max-produtos`: Número máximo de produtos com abas individuais no Excel (padrão: 20)
   - `--encoding`: Se seu arquivo contém caracteres especiais (padrão: utf-8)
   - `--verbose`: Mostra mais informações durante o processamento

4. **Aguarde o processamento**:
   - A ferramenta vai carregar seus dados, analisar todas as transações e gerar um relatório detalhado
   - No final, ela informará onde o relatório foi salvo

### Entendendo o Relatório

Após a execução bem-sucedida, você terá um arquivo Excel com várias abas:

1. **Aba "Resumo"**:
   - Lista todos os produtos ordenados por frequência
   - Mostra quantas vezes cada produto foi vendido
   - Apresenta a porcentagem de cada produto no total de vendas

2. **Abas de Produtos Individuais** (uma para cada produto popular):
   - Revela quais outros produtos são mais frequentemente comprados junto com este
   - Inclui gráficos visuais para facilitar a interpretação
   - Mostra a força de cada associação em porcentagem

3. **Aba "Rankings Completos"**:
   - Contém a lista completa de todas as associações para todos os produtos
   - Ordenada por produto principal e depois pela força da associação
   - Útil para análises mais detalhadas ou exportação para outros sistemas

4. **Aba "Insights e Recomendações"**:
   - Oferece sugestões práticas baseadas na análise
   - Inclui recomendações de marketing e disposição de produtos
   - Destaca oportunidades específicas de cross-selling

---

## 🚀 Exemplos de Uso

### Exemplo 1: Análise Básica

```bash
product-association-analysis vendas_2023.csv
```

Este comando simples analisará seu arquivo de vendas e criará um relatório Excel chamado `relatorio_associacoes.xlsx` no mesmo diretório.

### Exemplo 2: Análise Personalizada

```bash
product-association-analysis vendas_2023.csv --output relatorio_q1_2023.xlsx --max-produtos 10 --verbose
```

Este comando:
- Analisa o arquivo `vendas_2023.csv`
- Cria um relatório chamado `relatorio_q1_2023.xlsx`
- Limita o número de abas de produtos individuais a 10
- Mostra informações detalhadas durante o processamento

### Exemplo 3: Uso com Arquivos de Sistemas Diferentes

```bash
product-association-analysis dados_loja.csv --encoding latin1
```

Útil quando seu arquivo foi exportado de sistemas mais antigos ou que usam caracteres especiais (como acentos em português).

---

## ❓ Solução de Problemas

### "Arquivo não encontrado"
- **Problema**: O programa não consegue encontrar seu arquivo CSV
- **Solução**: Verifique se o caminho está correto. Tente colocar o arquivo na mesma pasta onde está executando o comando e usar apenas o nome do arquivo.

### "Erro de codificação"
- **Problema**: Caracteres estranhos aparecem nos dados
- **Solução**: Tente usar a opção `--encoding latin1` ou `--encoding cp1252` para arquivos exportados do Excel em português.

### "Colunas não encontradas"
- **Problema**: O programa não encontra as colunas necessárias
- **Solução**: Verifique se seu arquivo tem colunas chamadas "IdPedido" e "Produto". Se tiverem nomes diferentes, renomeie-as no Excel antes de exportar.

### "O Excel não abre o relatório"
- **Problema**: O arquivo é gerado, mas não abre
- **Solução**: Certifique-se de ter o Microsoft Excel ou LibreOffice Calc instalado. Tente abrir o Excel primeiro e depois abrir o arquivo através do menu Arquivo > Abrir.

---

## 👨‍💻 Para Desenvolvedores

Se você é um desenvolvedor e quer contribuir ou estender esta ferramenta:

### Usando como Biblioteca Python

```python
from product_association import carregar_dados, calcular_frequencia_produtos, identificar_transacoes, criar_ranking_associacoes, criar_excel_detalhado

# Carregar dados
df = carregar_dados('vendas.csv')

# Calcular frequência
contagem_produtos = calcular_frequencia_produtos(df)

# Identificar transações
transacoes, transacoes_multiplas = identificar_transacoes(df)

# Criar rankings de associações
associacoes = criar_ranking_associacoes(transacoes_multiplas, contagem_produtos)

# Gerar relatório
relatorio = criar_excel_detalhado(associacoes, contagem_produtos, 'relatorio.xlsx')
```

### Estendendo a Funcionalidade

A ferramenta foi projetada para ser modular e facilmente extensível. Consulte o arquivo [CONTRIBUTING.md](CONTRIBUTING.md) para saber como contribuir com o projeto.

---

## 📄 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

---

<div align="center">
  <p><b>Transforme seus dados em insights acionáveis!</b></p>
  <p>Feito com ❤️ pela comunidade de contribuidores</p>
</div>