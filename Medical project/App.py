from flask import Flask, render_template, request, redirect, url_for, session
from flask import Flask, render_template, send_from_directory, jsonify
import joblib
import numpy as np

app = Flask(__name__)
app.secret_key = 'naanu_bekku'

model = joblib.load("random_forest_model.pkl")

USERNAME = "user1"
PASSWORD = "password"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username == USERNAME and password == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index')) 
        else:
            return render_template('login.html', error="Invalid username or password")

    return render_template('login.html')


@app.route('/index')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/predict_page')
def predict_page():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('predict.html')

@app.route('/predict', methods=['POST'])
def predict():
    if not session.get('logged_in'):
        return redirect(url_for('login'))

    try:
        age = float(request.form['age'])
        sex = int(request.form['sex'])
        bmi = float(request.form['bmi'])
        children = int(request.form['children'])
        smoker = int(request.form['smoker'])
        region = int(request.form['region'])

        input_data = np.array([[age, sex, bmi, children, smoker, region]])
        predicted_cost = model.predict(input_data)[0]

        return jsonify({"prediction": f"Predicted Medical Cost per year: ₹{predicted_cost:.2f}"})

    except Exception as e:
        return jsonify({"error": str(e)})

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)