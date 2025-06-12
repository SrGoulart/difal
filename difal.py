# DIFAL Calculator - Python Script Version (com visual Streamlit)

import pandas as pd
import streamlit as st

def get_estado_aliquotas():
    estados = [
        'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS',
        'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN', 'RS', 'RO', 'RR', 'SC',
        'SP', 'SE', 'TO'
    ]
    estados_7 = ['MG', 'PR', 'RS', 'RJ', 'SC', 'SP']
    aliquotas = [7 if estado in estados_7 else 12 for estado in estados]
    return pd.DataFrame({
        'Estado': estados,
        'AliquotaInterestadual': aliquotas
    })


def calcular_difal(valor_produto_df, valor_produto_fora, frete_df, frete_ou, estado_origem, importado):
    aliquotas = get_estado_aliquotas()
    try:
        aliq_origem = 4 if importado else aliquotas.loc[aliquotas['Estado'] == estado_origem, 'AliquotaInterestadual'].values[0]
    except IndexError:
        return {'Erro': f"Estado '{estado_origem}' não encontrado."}

    aliq_destino = 20
    base_calculo_fora = valor_produto_fora
    difal = base_calculo_fora * ((aliq_destino - aliq_origem) / 100)
    total_df = valor_produto_df + frete_df
    total_outro_estado = valor_produto_fora + frete_ou + difal
    comparativo = 'Compra no DF é mais vantajosa' if total_df < total_outro_estado else 'Compra em outro estado é mais vantajosa'
    diferenca = abs(total_df - total_outro_estado)

    return {
        'Aliquota Estado de Origem (%)': aliq_origem,
        'Aliquota DF (%)': aliq_destino,
        'Aliquota Difal (%)': aliq_destino -  aliq_origem,
        'DIFAL (R$)': round(difal, 2),
        'Total Compra no DF (R$)': round(total_df, 2),
        'Total Compra Outro Estado (R$)': round(total_outro_estado, 2),
        'Comparativo': comparativo,
        'Diferença de Custo (R$)': round(diferenca, 2)
    }

# Interface Streamlit
st.title("Simulador de DIFAL - Dashboard")

valor_produto_df = st.number_input("Valor do Produto DF (R$)", min_value=0.0, step=0.01, format="%.2f")
valor_produto_fora = st.number_input("Valor do Produto fora do DF (R$)", min_value=0.0, step=0.01, format="%.2f")
frete_df = st.number_input("Frete - Compra no DF (R$)", min_value=0.0, step=0.01, format="%.2f")
frete_ou = st.number_input("Frete - Compra de Outro Estado (R$)", min_value=0.0, step=0.01, format="%.2f")
estado_origem = st.selectbox("Estado de Origem da Compra", get_estado_aliquotas()['Estado'])
importado = st.radio("Produto Importado?", options=[False, True], format_func=lambda x: "Sim" if x else "Não")

if st.button("Calcular"):
    resultado = calcular_difal(valor_produto_df, valor_produto_fora, frete_df, frete_ou, estado_origem, importado)
    if 'Erro' in resultado:
        st.error(resultado['Erro'])
    else:
        st.subheader("Resultado da Simulação")
        for chave, valor in resultado.items():
            st.write(f"**{chave}:** {valor}")
