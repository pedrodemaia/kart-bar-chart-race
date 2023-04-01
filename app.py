from flask import Flask, request
import subprocess

app = Flask(__name__)

@app.route('/process-link', methods=['POST'])
def process_link():
    link = request.form['link']
    output = subprocess.check_output(['python', 'main.py', link])
    return output

@app.route('/')
def home():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)
