from flask import Flask, render_template, redirect, request

app = Flask(__name__)

@app.route('/')
def home_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)


























































































""" CODE TO INCLUDE js AND css FILES IN html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}"

and

<script src="{{ url_for('static', filename='js/script.js') }}"></script>
"""