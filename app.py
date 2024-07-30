from flask import Flask, render_template, request, redirect, url_for, session

class AppData:
    def __init__(self):
        self.IsLoggedIn = False
        self.loggedInusername = None

class User:
    def __init__(self, name, surname, password):
        self.name = name
        self.surname = surname
        self.password = password   

app = Flask(__name__)
appData = AppData()
app.secret_key = 'supersecretkey'

# Простая база данных пользователей
users = {'user1': 'password1', 'user2': 'password2'}

users_data = {'user1': User('Ivan', 'Ivanov', 'password1'), 'user2': User('Hovannes', 'Hovhannisyan', 'password2')}

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET' and appData.IsLoggedIn:
        return redirect(url_for('profile'))
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users_data and users_data[username].password == password:
            appData.IsLoggedIn = True
            appData.loggedInusername = username
            return redirect(url_for('profile'))
        else:
            return render_template('login.html', error = 'Неверный логин или пароль')
    return render_template('login.html')

@app.route('/profile', methods = ['POST', 'GET'])
def profile():
    if appData.IsLoggedIn == False:
        return redirect(url_for('login'))
    if request.method == 'POST':
        users_data[appData.loggedInusername].name = request.form['name']
        users_data[appData.loggedInusername].surname = request.form['surname']
    return render_template('profile.html', username = appData.loggedInusername, name = users_data[appData.loggedInusername].name, surname = users_data[appData.loggedInusername].surname)

@app.route('/logout')
def logout():
    appData.IsLoggedIn = False
    return redirect('https://facebook.com')

@app.route('/changePassword', methods = ['GET', 'POST'])
def changePassword():
    if appData.IsLoggedIn == False:
        return redirect(url_for('login'))
    if request.method == 'POST':
        if request.form['old_password'] != users_data[appData.loggedInusername].password:
            return render_template('changePassword.html', error='Неверный пароль')
        new_password = request.form['new_password']
        repeat_new_password = request.form['repeat_new_password']
        special_symbol = {'.', ',', ':', ';', '!', '?', '(', ')', '[', ']', '{', '}', '<', '>', '+', '=', '-', '*', '%', '/', '$', '^', '|', '@', '#', '&', '_', '~', '`'} 
        if repeat_new_password != new_password:
            return render_template('changepassword.html', error='Пароли не совпадают')
        elif len(repeat_new_password) < 8:
            return render_template('changepassword.html', error='Пароль слишком короткий, его длина должна быть не менее 8 символов.')
        elif not any(character.isdigit() for character in repeat_new_password):    
            return render_template('changepassword.html', error='Пароль должен содержать хотя бы одну цифру.')
        elif not any(char.isupper() for char in repeat_new_password): 
            return render_template('changepassword.html', error='Пароль должен содержать хотя бы одну заглавную букву.')
        elif not any(char in special_symbol for char in repeat_new_password):
            return render_template('changepassword.html', error='Пароль должен содержать хотя бы один специальный символ.')
        users_data[appData.loggedInusername].password = request.form['new_password']
        return redirect(url_for('profile'))       
    return render_template('changePassword.html')    
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET' and appData.IsLoggedIn:
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
        special_symbol = {'.', ',', ':', ';', '!', '?', '(', ')', '[', ']', '{', '}', '<', '>', '+', '=', '-', '*', '%', '/', '$', '^', '|', '@', '#', '&', '_', '~', '`'} 
        if len(password) < 8:
            return render_template('register.html', error='Пароль слишком короткий, его длина должна быть не менее 8 символов.')
        elif not any(character.isdigit() for character in password):    
            return render_template('register.html', error='Пароль должен содержать хотя бы одну цифру.')
        elif not any(char.isupper() for char in password): 
            return render_template('register.html', error='Пароль должен содержать хотя бы одну заглавную букву.')
        elif not any(char in special_symbol for char in password):
            return render_template('register.html', error='Пароль должен содержать хотя бы один специальный символ.')
        elif username in users_data:
            return render_template('register.html', error='Пользователь с таким именем уже существует')
        if repeat_password != password:
            return render_template('register.html', error='Пароли не совпадают')
        users_data[username] = User(None, None, password)
        appData.IsLoggedIn = True
        appData.loggedInusername = username
        return redirect(url_for('profile'))
    return render_template('register.html')

if __name__ == '__main__':
    app.run()
    