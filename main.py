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

@st.cache_data #usa o cache para não ficar carregando os dados o tempo todo
def carregar_tickers_acoes():
    base_tickers = pd.read_csv("IBOV.csv", sep=";") #neste caso como o separador é ; foi necessário passar o sep
    tickers = list(base_tickers["Código"]) #transformando a planilha em uma lista python para montar os gráficos
    tickers = [item + ".SA" for item in tickers] #concatenando .SA no final de cada item da lista (list comprehension)
    return tickers

acoes = carregar_tickers_acoes()
dados = carregar_dados(acoes)
#print(dados)

# Exibir as colunas disponíveis
#st.write("Colunas disponíveis:", dados.columns.tolist())

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

# criar o título para performance dos ativos

# calculo de perfomance
texto_performance_ativos = ""

if len(lista_acoes)==0:
    lista_acoes = list(dados.columns)
elif len(lista_acoes)==1:
    dados = dados.rename(columns={"Close": acao_unica}) #quando não encontra a ação na lista, renomeia Close para acao_unica


carteira = [1000 for acao in lista_acoes] #para cada ação na minha lista de ações eu tenho R$1.000,00
total_inicial_carteira = sum(carteira)

for i, acao in enumerate(lista_acoes): #enumerate pega também o índice para mostrar a posição da acao na lista_acoes
    performance_ativo = dados[acao].iloc[-1] / dados[acao].iloc[0] - 1
    performance_ativo = float(performance_ativo)

    carteira[i] = carteira[i] * (1 + performance_ativo)

    if performance_ativo > 0:
        # :cor[texto]
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :green[{performance_ativo:.1%}]"
    elif performance_ativo < 0:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: :red[{performance_ativo:.1%}]"
    else:
        texto_performance_ativos = texto_performance_ativos + f"  \n{acao}: {performance_ativo:.1%}"

total_final_carteira = sum(carteira)
performance_carteira = total_final_carteira / total_inicial_carteira - 1

if performance_carteira > 0:
    texto_performance_carteira = f"Performance da carteira com todos os ativos: :green[{performance_carteira:.1%}]"
elif performance_carteira < 0:
    texto_performance_carteira = f"Performance da carteira com todos os ativos: :red[{performance_carteira:.1%}]"
else:
    texto_performance_carteira = f"Performance da carteira com todos os ativos: {performance_carteira:.1%}"



st.write(f"""
### Performance dos Ativos
Essa foi a perfomance de cada ativo no período selecionado:

{texto_performance_ativos}

{texto_performance_carteira}
""")


