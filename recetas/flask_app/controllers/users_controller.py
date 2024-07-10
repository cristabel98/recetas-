from flask import Flask, render_template, redirect, request, session, flash
from flask_app import app
from datetime import datetime

#Importamos todos los modelos
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

#Importación de BCrypt -> Encriptar la contraseña
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    #request.form = {"first_name": "Elena", "last_name": "De Troya"...}

    #Validar la info que estamos recibiendo
    if not User.validate_user(request.form):
        #No es válida la info, redireccionamos al formulario
        return redirect('/')    
    
    #Encriptamos la contraseña
    pass_encrypt = bcrypt.generate_password_hash(request.form['password'])
    #Generar un diccionario con toda la info del formulario
    form = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": pass_encrypt
    }

    id = User.save(form) #Recibo a cambio el ID del nuevo usuario
    session['user_id'] = id #Guardamos en sesión el identificador del usuario
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    #Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')

    #Crear una instancia del usuario. ID en sesión (session['user_id'])
    #Función que en base al ID regrese la instancia del usuario
    form = {"id": session['user_id']}
    user = User.get_by_id(form)

    #Lista de Recetas
    recipes = Recipe.get_all()

    return render_template('dashboard.html', user=user, recipes=recipes, now=datetime.utcnow)

@app.route('/login', methods=['POST'])
def login():
    #request.form = {"email": "elena@codingdojo.com", "password": "Hola123"}
    #Verificamos que el email exista en mi BD
    user = User.get_by_email(request.form) #Recibo False o recibo instancia de usuario

    if not user: #Si user = False
        flash('E-mail no registrado', 'login')
        return redirect('/')
    
    #Si user es instancia
    #user = OBJETO User .id=1, .first_name="Elena", .last_name ="De Troya"..... .password = "$2asdadjaodiajidjasj"
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Password incorrecto', 'login')
        return redirect('/')
    
    session['user_id'] = user.id #Guardo en mi sesión el id del usuario
    return redirect('/dashboard')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')