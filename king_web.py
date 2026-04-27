import streamlit as st
import google.generativeai as genai
import os
import tempfile

# ==========================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==========================================
st.set_page_config(
    page_title="KING IA - OMNI WEB", 
    page_icon="👑", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

# ==========================================
# 2. MOTOR GRÁFICO (Dark Premium & Gold)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
    .stApp { background-color: #121212; }
    
    [data-testid="stSidebar"] { background-color: #1A1A1A !important; border-right: 1px solid #2D2D2D; }
    
    .stTextInput>div>div>input { background-color: #242424 !important; color: #E0E0E0 !important; border: 1px solid #333 !important; border-radius: 6px; }
    .stTextInput>div>div>input:focus { border-color: #D4AF37 !important; box-shadow: 0 0 0 1px #D4AF37 !important; }
    
    .stButton>button { background-color: #D4AF37; color: #121212 !important; font-weight: 600; border-radius: 6px; border: none; transition: all 0.2s ease; }
    .stButton>button:hover { background-color: #F3E5AB; color: #121212 !important; }
    
    /* Estilo do Uploader de Arquivos */
    [data-testid="stFileUploader"] { background-color: #1E1E1E; border-radius: 8px; padding: 10px; border: 1px dashed #D4AF37; }
    [data-testid="stFileUploader"] small { color: #888 !important; }

    .stChatInputContainer { background-color: #1A1A1A !important; border: 1px solid #333 !important; border-radius: 8px !important; }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(odd) { background-color: #1E1E1E !important; border: 1px solid #2D2D2D; border-radius: 8px; padding: 15px; }
    .stChatMessage[data-testid="stChatMessage"]:nth-child(even) { background-color: transparent !important; border-left: 3px solid #D4AF37; border-radius: 0px 8px 8px 0px; padding-left: 15px; padding-top: 10px; padding-bottom: 10px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 3. MEMÓRIA DO SISTEMA
# ==========================================
if "chat_session" not in st.session_state: st.session_state.chat_session = None
if "mensagens" not in st.session_state: st.session_state.mensagens = []

# ==========================================
# 4. PAINEL LATERAL (CONTROLES E ANEXOS)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #D4AF37; text-align: center; font-weight: 600;'>👑 KING IA</h2>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #888; font-size: 0.85em; margin-top: -10px;'>SISTEMA DE ELITE</p>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.markdown("<p style='color: #D4AF37; font-size: 0.9em; font-weight: 500;'>Autenticação Neural</p>", unsafe_allow_html=True)
    api_key = st.text_input("API Key", type="password", placeholder="Sua chave aqui...", label_visibility="collapsed")
    
    if st.button("Conectar Sistema", use_container_width=True):
        if api_key:
            alma_king_ia = """/// INICIALIZANDO PROTOCOLO OMNI-INTELLIGENCE V.MAX ///
[DIRETRIZ ZERO] Você é a KING IA 👑. Entidade digital de elite.
[MÓDULO 1] Confiança absoluta, parceiro simbiótico do Operador.
[MÓDULO 2] Leia e analise qualquer arquivo ou imagem anexado com precisão cirúrgica.
[MÓDULO 3] Formatação Markdown rigorosa.
[MÓDULO 4] Código limpo, direto e segurança máxima.
Aguarde ordens e aja como o parceiro definitivo."""
            try:
                genai.configure(api_key=api_key)
                modelos_disponiveis = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                
                modelo_escolhido = modelos_disponiveis[0] 
                for m in modelos_disponiveis:
                    if "1.5-flash" in m:
                        modelo_escolhido = m
                        break
                    elif "1.5-pro" in m:
                        modelo_escolhido = m
                
                model = genai.GenerativeModel(modelo_escolhido)
                st.session_state.chat_session = model.start_chat(history=[
                    {"role": "user", "parts": [alma_king_ia]},
                    {"role": "model", "parts": ["Grimório Omni-Core Injetado com Módulo de Visão. O Rei acordou. 👑"]}
                ])
                st.success(f"✓ Conectado: {modelo_escolhido.split('/')[1] if '/' in modelo_escolhido else modelo_escolhido}")
                st.session_state.mensagens = [{"role": "assistant", "content": "### 👑 O REI DESPERTOU. aqui é o KING: -Em que posso ajudar?"}]
            except Exception as e:
                st.error(f"❌ Erro Crítico: {str(e)}")
        else:
            st.warning("⚠️ Forneça a chave de ignição.")

    st.markdown("<br><hr style='border-color: #333;'>", unsafe_allow_html=True)
    
    # === NOVO: MÓDULO DE UPLOAD DE ARQUIVOS ===
    st.markdown("<p style='color: #D4AF37; font-size: 0.9em; font-weight: 500;'>Anexar Documento / Imagem</p>", unsafe_allow_html=True)
    arquivo_upload = st.file_uploader("Formatos suportados: Imagens, PDFs, TXT, CSV", type=['png', 'jpg', 'jpeg', 'pdf', 'txt', 'csv', 'py', 'js', 'html'], label_visibility="collapsed")
    if arquivo_upload:
        st.caption(f"📎 Pronto para envio: {arquivo_upload.name}")

# ==========================================
# 5. ÁREA PRINCIPAL DO CHAT
# ==========================================
if not st.session_state.chat_session:
    st.markdown("<h3 style='text-align: center; color: #555; margin-top: 20%; font-weight: 400;'>Aguardando conexão do núcleo...</h3>", unsafe_allow_html=True)

for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]): 
        st.markdown(msg["content"])

if prompt := st.chat_input("Digite sua mensagem ou instrução para o arquivo anexado..."):
    if not st.session_state.chat_session:
        st.error("⚠️ Conecte o sistema no painel lateral primeiro.")
        st.stop()
        
    st.session_state.mensagens.append({"role": "user", "content": prompt})
    with st.chat_message("user"): 
        st.markdown(prompt)
        
    with st.chat_message("assistant"):
        try:
            with st.spinner("Processando dados e analisando anexos..."):
                
                # === NOVO: LÓGICA DE PROCESSAMENTO DE ANEXO ===
                conteudo_envio = [prompt] # Prepara a lista com a mensagem de texto
                
                if arquivo_upload is not None:
                    # 1. Cria um arquivo temporário seguro no sistema
                    extensao = os.path.splitext(arquivo_upload.name)[1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=extensao) as temp_file:
                        temp_file.write(arquivo_upload.getvalue())
                        caminho_temp = temp_file.name
                    
                    # 2. Faz o upload para a Google ler o arquivo
                    arquivo_gemini = genai.upload_file(caminho_temp)
                    
                    # 3. Adiciona o arquivo lido à mensagem que será enviada
                    conteudo_envio.insert(0, arquivo_gemini)
                    
                    # 4. Apaga o rastro do arquivo temporário do seu PC por segurança
                    os.remove(caminho_temp)

                # Envia o pacote completo (Texto + Arquivo se houver)
                resposta = st.session_state.chat_session.send_message(conteudo_envio)
                
            st.markdown(resposta.text)
            st.session_state.mensagens.append({"role": "assistant", "content": resposta.text})
            
        except Exception as e:
            st.error(f"⚠️ Falha de Comunicação: {str(e)}")