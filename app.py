import streamlit as st
from random import randrange

# Configuração da página
st.set_page_config(page_title="Jogo da Velha Python", page_icon="🎮", layout="centered")

st.markdown("<h1 style='text-align: center; color: #2c3e50;'>🎮 Jogo da Velha Python</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Jogue contra o computador direto no Streamlit!</p>", unsafe_allow_html=True)

# Inicialização do estado do jogo
if 'board' not in st.session_state:
    st.session_state.board = [[3 * j + i + 1 for i in range(3)] for j in range(3)]
    st.session_state.board[1][1] = 'X' # Coloca o primeiro 'X' no meio
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

# Botão de Reiniciar
col_r1, col_r2, col_r3 = st.columns([1, 2, 1])
with col_r2:
    if st.button("🔄 Reiniciar Jogo", use_container_width=True):
        st.session_state.board = [[3 * j + i + 1 for i in range(3)] for j in range(3)]
        st.session_state.board[1][1] = 'X'
        st.session_state.game_over = False
        st.session_state.winner = None
        st.rerun()

st.write("")

# Renderização do Tabuleiro
board = st.session_state.board

for row in range(3):
    cols = st.columns(3)
    for col in range(3):
        cell_value = board[row][col]
        
        if cell_value in ['X', 'O'] or st.session_state.game_over:
            cols[col].button(f"{cell_value}", key=f"btn_{row}_{col}", disabled=True)
        else:
            if cols[col].button(f"{cell_value}", key=f"btn_{row}_{col}"):
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

# Exibição de Status / Resultado
if st.session_state.game_over:
    if st.session_state.winner == 'you':
        st.success("🎉 Parabéns! Você venceu!")
    elif st.session_state.winner == 'me':
        st.error("🤖 O computador venceu! Mais sorte na próxima.")
    else:
        st.warning("🤝 O jogo terminou em Empate!")
else:
    st.info("Sua vez de jogar! Escolha um número no tabuleiro. (Você é o 'O')")
