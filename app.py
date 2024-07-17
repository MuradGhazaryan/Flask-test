from flask import Flask, render_template, request, redirect, url_for, session

class AppData:
    def __init__(self):
        self.IsLoggedIn = False

app = Flask(__name__)
appData = AppData()
app.secret_key = 'supersecretkey'

# Простая база данных пользователей
users = {'user1': 'password1', 'user2': 'password2'}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username] == password:
            return redirect(url_for('profile'))
        else:
            return "Неверный логин или пароль"
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/logout')
def logout():
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
