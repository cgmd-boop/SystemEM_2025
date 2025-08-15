import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Inicialização de dados em sessão
if "quedas" not in st.session_state:
    st.session_state.quedas = []

if "contas" not in st.session_state:
    st.session_state.contas = []

if "manutencoes" not in st.session_state:
    st.session_state.manutencoes = []

st.title("📊 Sistema de Gestão de Energia e Recursos")

# Seções do sistema
menu = st.sidebar.selectbox("Escolha uma seção", [
    "Registrar Queda de Energia",
    "Registrar Conta",
    "Agendar Manutenção",
    "Visualizar Gráficos",
    "Análise e Sugestões",
    "Relatório"
])

# Registrar queda de energia
if menu == "Registrar Queda de Energia":
    st.header("⚡ Registrar Queda de Energia")
    data = st.date_input("Data da queda")
    hora_queda = st.time_input("Horário da queda")
    hora_retorno = st.time_input("Horário de retorno")
    causa = st.selectbox("Causa", ["interna", "externa"])
    protocolo = st.text_input("Protocolo (se causa for externa)")
    if st.button("Registrar Queda"):
        st.session_state.quedas.append({
            "data": data,
            "hora_queda": hora_queda,
            "hora_retorno": hora_retorno,
            "causa": causa,
            "protocolo": protocolo if causa == "externa" else None
        })
        st.success("Queda registrada com sucesso!")

# Registrar conta
elif menu == "Registrar Conta":
    st.header("💰 Registrar Conta de Água/Energia")
    tipo = st.selectbox("Tipo de conta", ["energia", "água"])
    data = st.date_input("Data da conta")
    valor = st.number_input("Valor (R$)", min_value=0.0, step=0.01)
    multa = st.checkbox("Houve multa?")
    if st.button("Registrar Conta"):
        st.session_state.contas.append({
            "tipo": tipo,
            "data": data,
            "valor": valor,
            "multa": multa
        })
        st.success("Conta registrada com sucesso!")

# Agendar manutenção
elif menu == "Agendar Manutenção":
    st.header("🛠️ Agendar Manutenção")
    tipo = st.selectbox("Tipo", ["corretiva", "preditiva"])
    data = st.date_input("Data da manutenção")
    motivo = st.text_input("Motivo")
    status = st.selectbox("Status", ["andamento", "parado", "finalizado"])
    if st.button("Agendar"):
        st.session_state.manutencoes.append({
            "tipo": tipo,
            "data": data,
            "motivo": motivo,
            "status": status
        })
        st.success("Manutenção agendada com sucesso!")

# Visualizar gráficos
elif menu == "Visualizar Gráficos":
    st.header("📈 Gráficos de Contas")
    if st.session_state.contas:
        df = pd.DataFrame(st.session_state.contas)
        df["mes"] = df["data"].apply(lambda x: x.strftime("%b/%Y"))
        grouped = df.groupby(["mes", "tipo"])["valor"].sum().unstack().fillna(0)
        st.line_chart(grouped)
    else:
        st.info("Nenhuma conta registrada para gerar gráfico.")

# Análise e sugestões
elif menu == "Análise e Sugestões":
    st.header("🔍 Análise de Quedas de Energia")
    total = len(st.session_state.quedas)
    externas = sum(1 for q in st.session_state.quedas if q["causa"] == "externa")
    internas = total - externas
    st.write(f"Total de quedas registradas: {total}")
    st.write(f"Quedas internas: {internas}")
    st.write(f"Quedas externas: {externas}")
    if total == 0:
        st.warning("Nenhuma queda registrada.")
    elif internas > externas:
        st.error("⚠️ Muitas quedas internas. Sugestão: revisar equipamentos.")
    elif externas > internas:
        st.warning("📡 Muitas quedas externas. Sugestão: acompanhar protocolos da concessionária.")
    else:
        st.success("✅ Quedas equilibradas. Situação estável.")

# Relatório
elif menu == "Relatório":
    st.header("📄 Relatório Geral")
    st.subheader("Quedas de Energia")
    st.write(pd.DataFrame(st.session_state.quedas))
    st.subheader("Contas Registradas")
    st.write(pd.DataFrame(st.session_state.contas))
    st.subheader("Manutenções Agendadas")
    st.write(pd.DataFrame(st.session_state.manutencoes))

#Adiciona sistema interativo com Streamlit
