# importar as bibliotecas
import streamlit as st
import pandas as pd
import yfinance as yf
from datetime import timedelta

# Para executar o streamlit, no terminal digite
# streamlit run main.py

# criar as funções de carregamento de dados
# cotações do Itau - ITUB4 - 2010 a 2024
@st.cache_data
def carregar_dados(empresas):
    texto_tickers = " ".join(empresas) #junta todas empresas em uma string separando por espaços
    dados_acao = yf.Tickers(texto_tickers) #todos ativos da bolsa brasileira terminam com .SA, que é a bolsa de São Paulo
    cotacoes_acao = dados_acao.history(period="1d", start="2010-01-01", end="2024-07-01")
    #print(cotacoes_acao)
    cotacoes_acao = cotacoes_acao["Close"] #com 2 colchetes ele retornar uma lista de valores com o índice que é a coluna Date
    return cotacoes_acao

acoes = ["ITUB4.SA", "PETR4.SA", "MGLU3.SA", "VALE3.SA", "ABEV3.SA", "GGBR4.SA"]
dados = carregar_dados(acoes)
#print(dados)

# criar a interface do streamlit
# para rodar o programa tem que digitar no termina: streamlit run main.py
st.write("""
# App Preço de Ações
O gráfico abaixo representa a evolução de preços das ações ao longo do ano de 2010 e 2024
 """) #pode formatar no modelo markdown (usar # para tamanho do texto)

# preparar as visualizações

st.sidebar.header("Filtros") #cria a barra lateral que coloca todos filtros na lateral


#Filtro de Ações
lista_acoes = st.sidebar.multiselect("Escolha as ações para visualizar", dados.columns) #lista de ações com os nomes para formar as colunas
if lista_acoes:
    dados = dados[lista_acoes]
    if len(lista_acoes) == 1:
        acao_unica = lista_acoes[0]
        dados = dados.rename(columns={acao_unica: "Close"})

#Filtro de Datas
data_inicial = dados.index.min().to_pydatetime() #o campo data é o índice da tabela. Pega a menor data
data_final = dados.index.max().to_pydatetime()# pega a maior data da tabela
intervalo_data = st.sidebar.slider("Selecione o Período", 
                                   min_value=data_inicial, 
                                   max_value=data_final, 
                                   value=(data_inicial, data_final),
                                   step=timedelta(days=1)) #value é o valor inicial. Passando uma tupla para pegar o intervalo. step pode passar por exemplo 15 em 15 dias

#Aplicando Filtro. [0] perído inicial e [1] período final do intervalo
print(intervalo_data)
dados = dados.loc[intervalo_data[0] : intervalo_data[1]]  #filtra as linhas de acordo com o índice da tabela, que é a data

# criar o gráfico
st.line_chart(dados)

