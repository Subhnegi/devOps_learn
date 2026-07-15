from flask import Flask, render_template, request
import requests
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']
    print(f"Received sign-up request with email: {email} and password: {password}")
    try:
        response = requests.post('http://localhost:5000/api/signup', json={'email': email, 'password': password})
        if response.status_code == 200:
            return render_template('success.html', message='Data submitted successfully')
        else:
            return render_template('index.html', error='Invalid email or password')
    except Exception as e:
        print(f"Error occurred: {e}")
        return render_template('index.html', error='An error occurred while processing your request')

if __name__ == '__main__':
    app.run(port=5001, debug=True)
