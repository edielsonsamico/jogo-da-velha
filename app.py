import streamlit as st
from random import randrange

# Configuração da página e layout centralizado
st.set_page_config(page_title="Jogo da Velha Tradicional", page_icon="🎲", layout="centered")

# Estilos CSS avançados para simular um tabuleiro real com linhas de grade
st.markdown("""
    <style>
    .main-title {
        text-align: center;
        font-family: 'Helvetica Neue', sans-serif;
        color: #2c3e50;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .subtitle {
        text-align: center;
        color: #7f8c8d;
        margin-bottom: 25px;
        font-size: 16px;
    }
    /* Estilização profissional dos botões do tabuleiro simulando casas reais */
    div.stButton > button {
        width: 100%;
        height: 110px;
        font-size: 48px;
        font-weight: bold;
        border-radius: 12px;
        border: 3px solid #34495e;
        background-color: #fdfefe;
        color: #2c3e50;
        box-shadow: 0 4px 8px rgba(0,0,0,0.08);
        transition: all 0.15s ease-in-out;
    }
    div.stButton > button:hover {
        border-color: #2980b9;
        background-color: #ebf5fb;
        transform: scale(1.02);
    }
    /* Estilo para destacar o botão de reiniciar */
    .stButton.restart-btn > button {
        height: 50px;
        font-size: 18px;
        background-color: #2c3e50;
        color: white;
        border: none;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='main-title'>🎲 Jogo da Velha Tradicional</h1>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A experiência clássica de tabuleiro direto no seu navegador</div>", unsafe_allow_html=True)

# Inicialização do estado do jogo
if 'board' not in st.session_state:
    st.session_state.board = [[3 * j + i + 1 for i in range(3)] for j in range(3)]
    st.session_state.board[1][1] = 'X'  # O computador começa no centro
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

# Estrutura centralizada simulando a moldura do tabuleiro real
_, col_center, _ = st.columns([1, 2.8, 1])

with col_center:
    # Botão de Nova Partida
    if st.button("🔄 Nova Partida", use_container_width=True):
        st.session_state.board = [[3 * j + i + 1 for i in range(3)] for j in range(3)]
        st.session_state.board[1][1] = 'X'
        st.session_state.game_over = False
        st.session_state.winner = None
        st.rerun()

    st.write("")

    # Renderização das 3 linhas e 3 colunas formandos a grelha do tabuleiro
    board = st.session_state.board
    for row in range(3):
        cols = st.columns(3)
        for col in range(3):
            cell_value = board[row][col]
            
            # Formatação visual das peças no tabuleiro
            if cell_value == 'O':
                display_text = "🔵"  # Sua peça (Azul)
            elif cell_value == 'X':
                display_text = "❌"  # Peça do Computador (Vermelho/Cruz)
            else:
                display_text = str(cell_value)  # Número da casa vazia

            # Renderiza o botão correspondente à casa do tabuleiro
            if cell_value in ['X', 'O'] or st.session_state.game_over:
                cols[col].button(display_text, key=f"cell_{row}_{col}", disabled=True)
            else:
                if cols[col].button(display_text, key=f"cell_{row}_{col}"):
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

    # Painel de Status / Resultado da Partida
    if st.session_state.game_over:
        if st.session_state.winner == 'you':
            st.success("🎉 Vitória espetacular! Você venceu o jogo!")
        elif st.session_state.winner == 'me':
            st.error("🤖 O computador fechou o espaço e venceu!")
        else:
            st.warning("🤝 Fim de jogo: Empate técnico no tabuleiro!")
    else:
        st.info("Sua vez de jogar! Clique em um número para posicionar sua peça (🔵).")
