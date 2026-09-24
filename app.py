import streamlit as st
from random import randrange

# Configuração da página e layout
st.set_page_config(page_title="Jogo da Velha Moderno", page_icon="🎮", layout="centered")

# Estilos CSS personalizados para um visual incrível
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        color: #1f77b4;
        font-weight: 700;
        margin-bottom: 5px;
    }
    .subtitle {
        text-align: center;
        color: #666;
        margin-bottom: 30px;
    }
    /* Estilo customizado para os botões do tabuleiro */
    div.stButton > button {
        width: 100%;
        height: 100px;
        font-size: 42px;
        font-weight: bold;
        border-radius: 15px;
        border: 2px solid #e2e8f0;
        background-color: #ffffff;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        transition: all 0.2s ease-in-out;
    }
    div.stButton > button:hover {
        border-color: #3182ce;
        background-color: #ebf8ff;
        transform: translateY(-2px);
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🎮 Jogo da Velha</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Desafie a inteligência artificial direto no seu navegador!</div>", unsafe_allow_html=True)

# Inicialização do estado do jogo
if 'board' not in st.session_state:
    st.session_state.board = [[3 * j + i + 1 for i in range(3)] for j in range(3)]
    st.session_state.board[1][1] = 'X'  # Computador começa no meio
    st.session_state.game_over = False
    st.session_state.winner = None

def make_list_of_free_fields(board):
    free = []
    for row in range(3):
        for col in range(3):
            if board[row][col] not in ['O', 'X']:
                free.append((row, col))
    return free

def victory_for(board, sgn):
    if sgn == "X":
        who = 'me'
    elif sgn == "O":
        who = 'you'
    else:
        who = None
    
    cross1 = cross2 = True
    for rc in range(3):
        if board[rc][0] == sgn and board[rc][1] == sgn and board[rc][2] == sgn:
            return who
        if board[0][rc] == sgn and board[1][rc] == sgn and board[2][rc] == sgn:
            return who
        if board[rc][rc] != sgn:
            cross1 = False
        if board[2 - rc][2 - rc] != sgn:
            cross2 = False
    if cross1 or cross2:
        return who
    return None

def computer_turn():
    free = make_list_of_free_fields(st.session_state.board)
    if len(free) > 0 and not st.session_state.game_over:
        this = randrange(len(free))
        row, col = free[this]
        st.session_state.board[row][col] = 'X'
        
        victor = victory_for(st.session_state.board, 'X')
        if victor == 'me':
            st.session_state.game_over = True
            st.session_state.winner = 'me'
        elif len(make_list_of_free_fields(st.session_state.board)) == 0:
            st.session_state.game_over = True
            st.session_state.winner = 'tie'

# Centralizando o tabuleiro com colunas extras nas pontas
_, col_center, _ = st.columns([1, 3, 1])

with col_center:
    # Botão de Reiniciar alinhado
    if st.button("🔄 Reiniciar Partida", use_container_width=True):
        st.session_state.board = [[3 * j + i + 1 for i in range(3)] for j in range(3)]
        st.session_state.board[1][1] = 'X'
        st.session_state.game_over = False
        st.session_state.winner = None
        st.rerun()

    st.write("")

    # Renderização do Tabuleiro 3x3 em formato de grelha limpa
    board = st.session_state.board
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            cell_value = board[row][col]
            
            # Formatação visual das peças
            label = cell_value
            if cell_value == 'O':
                label = "🔵 O"
            elif cell_value == 'X':
                label = "❌ X"

            if cell_value in ['X', 'O'] or st.session_state.game_over:
                cols[col].button(label, key=f"btn_{row}_{col}", disabled=True)
            else:
                if cols[col].button(label, key=f"btn_{row}_{col}"):
                    st.session_state.board[row][col] = 'O'
                    
                    victor = victory_for(st.session_state.board, 'O')
                    if victor == 'you':
                        st.session_state.game_over = True
                        st.session_state.winner = 'you'
                    elif len(make_list_of_free_fields(st.session_state.board)) == 0:
                        st.session_state.game_over = True
                        st.session_state.winner = 'tie'
                    else:
                        computer_turn()
                    st.rerun()

    st.write("")

    # Mensagens de Status / Resultado estilizadas
    if st.session_state.game_over:
        if st.session_state.winner == 'you':
            st.success("🎉 Parabéns! Você venceu a partida!")
        elif st.session_state.winner == 'me':
            st.error("🤖 O computador levou a melhor desta vez!")
        else:
            st.warning("🤝 Empate! Jogo equilibrado.")
    else:
        st.info("Sua vez! Escolha uma casa numérica (Você é o 🔵 O).")
