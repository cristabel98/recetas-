#Importar la conexión con la BD
from flask_app.config.mysqlconnection import connectToMySQL

import re #Importación de Expresiones Regulares
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') #Expresion regular de email

from flask import flash #flash es el encargado de mostrar errores/mensajes

class User:

    def __init__(self, data):
        #data = {diccionario con toda la info que tiene la instancia}
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, form):
        #form = {"first_name": "Elena", "last_name": "De Troya", "email": "elena@cd.com", "password": "YA ESTE ENCRIPTADO"}
        query = "INSERT INTO users (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        result = connectToMySQL('esquema_recetas_aa').query_db(query, form)
        return result #El ID de nuevo registro que se realizó
    
    #Validar la info que recibimos en el formulario
    @staticmethod
    def validate_user(form):
        #form = {diccionario con todos los names y valores que el usuario ingresó}
        is_valid = True #Pretendemos que todo le formulario está llenado correctamente

        #Validamos que el nombre tenga al menos 2 caracteres
        if len(form['first_name']) < 2:
            flash('Nombre debe tener al menos 2 caracteres', 'register')
            is_valid = False
        
        #Validamos que el apellido tenga al menos 2 caracteres
        if len(form['last_name']) < 2:
            flash('Apellido debe tener al menos 2 caracteres', 'register')
            is_valid = False
        
        #Validamos que el password tenga al menos 6 caracteres
        if len(form['password']) < 6:
            flash('Contraseña debe tener al menos 6 caracteres', 'register')
            is_valid = False
        
        #Validamos que el correo sea único
        query = "SELECT * FROM users WHERE email = %(email)s"
        results = connectToMySQL('esquema_recetas_aa').query_db(query, form)
        if len(results) >=1:
            flash('E-mail registrado previamente', 'register')
            is_valid = False
        
        #Verificamos que las contraseñas coincidan
        if form['password'] != form['confirm']:
            flash('Contraseñas no coinciden', 'register')
            is_valid = False
        
        #Verificamos que el email tenga el formato correcto -> Expresiones Regulares
        if not EMAIL_REGEX.match(form['email']):
            flash('E-mail inválido', 'register')
            is_valid = False
        
        return is_valid
    
    @classmethod
    def get_by_email(cls, form):
        #form = {"email": "elena@codingdojo.com", "password": "Hola123"}
        query = "SELECT * FROM users WHERE email = %(email)s"
        result = connectToMySQL('esquema_recetas_aa').query_db(query, form) #SELECT me regresa una lista de diccionarios
        if len(result) < 1: #Significa que mi lista está vacía Y NO existe ese email en mi BD
            return False
        else:
            #Me regresa 1 registro
            #result = [ {"id": 1, "first_name": "Elena", "last_name": "De Troya"......} ]
            user = cls(result[0]) #User({"id": 1, "first_name": "Elena", "last_name": "De Troya"......})
            return user
    
    @classmethod
    def get_by_id(cls, form):
        #form = {"id": 1}
        query = "SELECT * FROM users WHERE id = %(id)s"
        result = connectToMySQL('esquema_recetas_aa').query_db(query, form) #Lista de diccionarios (que SOLO TIENE posicion 0)
        #result = [ {"id": 1, "first_name": "Elena", "last_name": "De Troya"......} ]
        user = cls(result[0])
        return user