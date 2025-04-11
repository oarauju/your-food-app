import streamlit as st
import requests

# Configuração da API Groq
token = "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"
api_url = "https://api.groq.com/openai/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# Configuração da interface
st.set_page_config(page_title="IA Financeira", page_icon="", layout="wide")
st.markdown("""
    <style>
        body { background-color: #0e0e0e; color: white; }
        .stTextInput input { background-color: #1c1c1c; color: white; border-radius: 10px; }
        .stChatMessage { background-color: #1c1c1c; padding: 10px; border-radius: 10px; margin-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("IA Financeira")
st.write("Pergunte sobre finanças, economia ou criptoativos:")

# Inicializar histórico
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Exibir histórico de mensagens
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Entrada do usuário
user_input = st.chat_input("Digite sua pergunta aqui...")
if user_input:
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)
    
    # Enviar para a API da Groq
    try:
        data = {
            "model": "meta-llama/llama-4-scout-17b-16e-instruct",
            "messages": [{"role": "user", "content": user_input}]
        }
        response = requests.post(api_url, headers=headers, json=data)
        response_json = response.json()
        
        if "error" in response_json:
            bot_response = f"❌ Erro: {response_json['error']}"
        elif "choices" in response_json and response_json["choices"]:
            bot_response = response_json["choices"][0]["message"]["content"]
        else:
            bot_response = "⚠️ Resposta inesperada da API."
    except Exception as e:
        bot_response = "⚠️ Erro na comunicação com a API. Verifique sua conexão e token."
    
    # Exibir resposta
    with st.chat_message("assistant"):
        st.markdown(bot_response)
    
    # Salvar no histórico
    st.session_state["messages"].append({"role": "assistant", "content": bot_response})
