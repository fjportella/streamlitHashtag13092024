# importar as bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf

# criar as funções de carregamento de dados
# cotações do Itau - ITUB4 - 2010 a 2024
@st.cache_data
def carregar_dados(empresa):
    dados_acao = yf.Ticker(empresa) #todos ativos da bolsa brasileira terminam com .SA, que é a bolsa de São Paulo
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-07-01")
    cotacoes_acao = cotacoes_acao[["Close"]] #com 2 colchetes ele retornar uma lista de valores com o índice que é a coluna Date
    return cotacoes_acao

# preparar as visualizações
dados = carregar_dados("ITUB4.SA")
#print(dados)


# criar a interface do streamlit
# para rodar o programa tem que digitar no termina: streamlit run main.py
st.write("""
# App Preço de Ações
O gráfico abaixo representa a evolução de preços de ações Itaú (ITUB4) ao longo do ano de 2010 e 2024
 """) #pode formatar no modelo markdown (usar # para tamanho do texto)

# criar o gráfico
st.line_chart(dados)



st.write("""
# Fim do app
""")