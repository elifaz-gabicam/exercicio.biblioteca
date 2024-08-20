from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketio = SocketIO(app)

# Estado do tabuleiro e controle de jogadores
board = ['' for _ in range(9)]
current_turn = 'X'

@app.route('/')
def index():
    return render_template('jogo.html')

@socketio.on('make_move')
def handle_move(data):
    global board, current_turn
    index = int(data['index'])  # Converte o índice para inteiro
    if board[index] == '':
        board[index] = current_turn
        emit('update_board', {'index': index, 'symbol': current_turn}, broadcast=True)
        if check_winner(current_turn):
            emit('game_over', {'winner': current_turn}, broadcast=True)
            reset_board()
        elif '' not in board:
            emit('game_over', {'winner': 'Empate'}, broadcast=True)
            reset_board()
        else:
            current_turn = 'O' if current_turn == 'X' else 'X'

def check_winner(symbol):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8], # Linhas
        [0, 3, 6], [1, 4, 7], [2, 5, 8], # Colunas
        [0, 4, 8], [2, 4, 6]             # Diagonais
    ]
    return any(all(board[i] == symbol for i in condition) for condition in win_conditions)

def reset_board():
    global board, current_turn
    board = ['' for _ in range(9)]
    current_turn = 'X'

if __name__ == '__main__':
    socketio.run(app, port=8000, debug=True)