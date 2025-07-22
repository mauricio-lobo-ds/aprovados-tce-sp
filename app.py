import streamlit as st
import pandas as pd
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Dashboard TCE-SP - Aprovados",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_data():
    """Carrega e processa os dados do CSV"""
    df = pd.read_csv('lista_tce.csv', sep=';', encoding='utf-8')
    
    # Converter data de nascimento para datetime
    df['DATA NASC'] = pd.to_datetime(df['DATA NASC'], format='%d/%m/%Y')
    
    # Garantir que NOTA e CE sejam numéricas
    df['NOTA'] = pd.to_numeric(df['NOTA'], errors='coerce')
    df['CE'] = pd.to_numeric(df['CE'], errors='coerce')
    
    return df

def sort_data(df):
    """Aplica a ordenação específica: NOTA desc, CE desc, DATA NASC asc (mais velhos primeiro)"""
    return df.sort_values(['NOTA', 'CE', 'DATA NASC'], ascending=[False, False, True])

def main():
    # Aplicar CSS para reduzir tamanhos gerais
    st.markdown("""
    <style>
    /* Reduzir tamanho do título principal */
    .main h1 {
        font-size: 1.8rem !important;
        margin-bottom: 1rem !important;
    }
    
    /* Reduzir tamanho dos subtítulos */
    .main h2, .main h3 {
        font-size: 1.3rem !important;
        margin-bottom: 0.8rem !important;
    }
    
    /* Reduzir tamanho da fonte dos dropdowns e labels na sidebar */
    .sidebar .stSelectbox label {
        font-size: 0.8rem !important;
    }
    
    .sidebar .stSelectbox div[data-baseweb="select"] {
        font-size: 0.8rem !important;
    }
    
    /* Reduzir tamanho das métricas e adicionar borda com sombra */
    .stMetric {
        background-color: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        padding: 0.5rem !important;
        margin: 0.2rem !important;
        min-height: 60px !important;
    }
    
    .stMetric > div {
        padding: 0.2rem !important;
    }
    
    .stMetric label {
        font-size: 0.6rem !important;
        font-weight: 500 !important;
        color: #666 !important;
    }
    
    .stMetric div[data-testid="stMetricValue"] > div {
        font-size: 1.1rem !important;
        font-weight: bold !important;
        line-height: 1.2 !important;
    }
    
    /* Alternativa mais específica */
    [data-testid="stMetric"] {
        background-color: white !important;
        border: 1px solid #e0e0e0 !important;
        border-radius: 8px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
        padding: 0.4rem !important;
    }
    
    /* Reduzir espaçamento geral */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 1rem !important;
    }
    
    /* Reduzir tamanho dos botões */
    .stButton button {
        font-size: 0.8rem !important;
        padding: 0.3rem 0.8rem !important;
    }
    
    /* Reduzir tamanho da fonte da sidebar */
    .sidebar .stMarkdown {
        font-size: 0.8rem !important;
    }
    
    /* Reduzir espaçamento na sidebar */
    .stSidebar .element-container {
        margin-bottom: 0.1rem !important;
    }
    
    .stSidebar .stSelectbox {
        margin-bottom: 0rem !important;
    }
    
    .stSidebar .stButton {
        margin-top: 0.5rem !important;
        margin-bottom: 0.1rem !important;
    }
    
    /* Reduzir espaçamento dos separadores na sidebar */
    .stSidebar hr {
        margin-top: 0.5rem !important;
        margin-bottom: 0.5rem !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Título principal
    st.title("📊 Dashboard TCE-SP - Candidatos Aprovados")
    st.markdown("---")
    
    # Carregar dados
    try:
        df = load_data()
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return
    
    # Sidebar com filtros
    st.sidebar.header("🔍 Filtros")
    
    # Filtro por CARGO
    cargos_disponiveis = ['Todos'] + sorted(df['CARGO'].unique().tolist())
    cargo_selecionado = st.sidebar.selectbox("Cargo:", cargos_disponiveis)
    
    # Filtro por LOCALIDADE
    localidades_disponiveis = ['Todas'] + sorted(df['LOCALIDADE'].unique().tolist())
    localidade_selecionada = st.sidebar.selectbox("Localidade:", localidades_disponiveis)
    
    # Filtro por NEGRO
    negro_opcoes = ['Todos', 'SIM', 'NAO']
    negro_selecionado = st.sidebar.selectbox("Negro (Cota Racial):", negro_opcoes)
    
    # Filtro por PCD
    pcd_opcoes = ['Todos', 'SIM', 'NAO']
    pcd_selecionado = st.sidebar.selectbox("PCD (Pessoa com Deficiência):", pcd_opcoes)
    
    # Filtro por STATUS
    status_opcoes = ['Todos', 'VAGA', 'CR']
    status_selecionado = st.sidebar.selectbox("Status (VAGA/CR):", status_opcoes)
    
    # Link para mostrar imagem de vagas
    st.sidebar.markdown("---")
    if st.sidebar.button("📊 Ver Distribuição de Vagas"):
        st.session_state.show_vagas_image = True
    
    # Aplicar filtros
    df_filtrado = df.copy()
    
    if cargo_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['CARGO'] == cargo_selecionado]
    
    if localidade_selecionada != 'Todas':
        df_filtrado = df_filtrado[df_filtrado['LOCALIDADE'] == localidade_selecionada]
    
    if negro_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['NEGRO'] == negro_selecionado]
    
    if pcd_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['PCD'] == pcd_selecionado]
    
    if status_selecionado != 'Todos':
        df_filtrado = df_filtrado[df_filtrado['STATUS'] == status_selecionado]
    
    # Créditos do desenvolvedor
    st.sidebar.markdown(
        "<small style='color: #888888;'>Dashboard desenvolvido por Mauricio Lobo</small>", 
        unsafe_allow_html=True
    )
    
    # Aplicar ordenação
    df_filtrado = sort_data(df_filtrado)
    
    # Verificar se deve mostrar a imagem de vagas
    if hasattr(st.session_state, 'show_vagas_image') and st.session_state.show_vagas_image:
        st.subheader("Distribuição de Vagas")
        
        # Botão para voltar à tabela (antes da imagem e com cor azul)
        st.markdown("""
        <style>
        div[data-testid="stButton"] > button[kind="secondary"] {
            background-color: #0066cc !important;
            color: white !important;
            border: none !important;
        }
        div[data-testid="stButton"] > button[kind="secondary"]:hover {
            background-color: #004499 !important;
            color: white !important;
        }
        </style>
        """, unsafe_allow_html=True)
        
        if st.button("← Voltar para Lista de Candidatos", key="voltar_blue"):
            st.session_state.show_vagas_image = False
            st.rerun()
        
        try:
            st.image("vagas.png", caption="Distribuição de Vagas TCE-SP", use_column_width=True)
                
        except FileNotFoundError:
            st.error("Imagem vagas.png não encontrada!")
            st.session_state.show_vagas_image = False
            st.rerun()
        
        return  # Para não mostrar a tabela quando estiver mostrando a imagem
    
    
    # Informações gerais (apenas quando não estiver mostrando a imagem)
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total de Registros", len(df_filtrado))
    
    with col2:
        st.metric("Cargos Únicos", df_filtrado['CARGO'].nunique())
    
    with col3:
        st.metric("Localidades Únicas", df_filtrado['LOCALIDADE'].nunique())
    
    with col4:
        if len(df_filtrado) > 0:
            nota_media = df_filtrado['NOTA'].mean()
            st.metric("Nota Média", f"{nota_media:.2f}")
    
    st.markdown("---")
    
    # Tabela principal
    st.subheader("📋 Lista de Candidatos Aprovados")
    
    # Critério de ordenação (com fonte menor)
    st.markdown("<small><strong>Critério de Ordenação:</strong> 1º NOTA (maior primeiro), 2º CE (maior primeiro), 3º DATA NASC (mais velhos primeiro)</small>", unsafe_allow_html=True)
    
    if len(df_filtrado) > 0:
        # Formatar a data para exibição
        df_display = df_filtrado.copy()
        df_display['DATA NASC'] = df_display['DATA NASC'].dt.strftime('%d/%m/%Y')
        
        # Adicionar coluna de posição/classificação
        df_display.insert(0, 'POSIÇÃO', range(1, len(df_display) + 1))
        
        
        # Função para aplicar cor de fundo baseada no STATUS
        def color_vagas(row):
            if row['STATUS'] == 'VAGA':
                return ['background-color: #d4edda'] * len(row)
            else:
                return [''] * len(row)
        
        # Aplicar styling
        df_styled = df_display.style.apply(color_vagas, axis=1)
        
        # Configurar a tabela com fonte menor
        st.markdown("""
        <style>
        .stDataFrame {
            font-size: 8px;
        }
        .stDataFrame table {
            font-size: 8px;
        }
        .stDataFrame th {
            font-size: 8px;
        }
        .stDataFrame td {
            font-size: 8px;
        }
        </style>
        """, unsafe_allow_html=True)
        
        st.dataframe(
            df_styled,
            use_container_width=True,
            height=600,
            hide_index=True,
            column_config={
                "POSIÇÃO": st.column_config.NumberColumn("Pos.", width="small"),
                "CARGO": st.column_config.TextColumn("Cargo", width="small"),
                "LOCALIDADE": st.column_config.TextColumn("Localidade", width="small"),
                "NOME": st.column_config.TextColumn("Nome", width="medium"),
                "INSCRICAO": st.column_config.TextColumn("Inscrição", width="small"),
                "DATA NASC": st.column_config.TextColumn("Data Nasc.", width="small"),
                "CG": st.column_config.NumberColumn("CG", width="small"),
                "CE": st.column_config.NumberColumn("CE", width="small"),
                "NOTA": st.column_config.NumberColumn("Nota", width="small"),
                "NEGRO": st.column_config.TextColumn("Negro", width="small"),
                "PCD": st.column_config.TextColumn("PCD", width="small"),
                "STATUS": st.column_config.TextColumn("Status", width="small")
            }
        )
        
        # Botão de download
        csv = df_display.to_csv(index=False, sep=';').encode('utf-8')
        st.download_button(
            label="📥 Baixar dados filtrados (CSV)",
            data=csv,
            file_name=f'tce_sp_filtrado_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv',
            mime='text/csv'
        )
        
    else:
        st.warning("Nenhum registro encontrado com os filtros aplicados.")

if __name__ == "__main__":
    main()