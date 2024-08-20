from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        player_choice = request.form['choice']
        computer_choice = random.choice(['Pedra', 'Papel', 'Tesoura'])
        result = determine_winner(player_choice, computer_choice)
        return render_template('index.html', player_choice=player_choice, computer_choice=computer_choice, result=result)
    return render_template('index.html')

def determine_winner(player, computer):
    if player == computer:
        return 'Empate'
    elif (player == 'Pedra' and computer == 'Tesoura') or \
         (player == 'Papel' and computer == 'Pedra') or \
         (player == 'Tesoura' and computer == 'Papel'):
        return 'Você venceu!'
    else:
        return 'Você perdeu!'

if __name__ == '__main__':
    app.run(debug=True)