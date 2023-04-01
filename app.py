'''
Web App para executar o kart bar chart race

Para chamar aplicação, rodar no terminal:
    poetry shhll
    set FLASK_APP=app.py
    flask run
Rodar com o comando em outro terminal: Invoke-WebRequest -Uri http://localhost:5000/gif -Method POST -Body @{string="http://www.mylaptime.com/laptime/clientes/214V20106819C9780G1X1P108/results/r3.html?evt=11303&epg=6512"}
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