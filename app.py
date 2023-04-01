'''
Web App para executar o kart bar chart race

Para chamar aplicação, rodar "python app.py" no terminal
Acessar a aplicação em localhost:5000
'''

import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/gif', methods=['POST'])
def get_gif():
    string = request.form['string']
    # Chamar o código Python que gera o GIF
    subprocess.Popen(['python', 'main.py', string], stdout=subprocess.PIPE)
    return jsonify({'gif': 'race_evolution.gif'})

if __name__ == '__main__':
    app.run()