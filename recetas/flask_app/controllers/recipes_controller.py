from flask import Flask, render_template, redirect, session, request, flash
from flask_app import app

#MODELOS
from flask_app.models.users import User
from flask_app.models.recipes import Recipe

#Importaciones para subir imágenes
from werkzeug.utils import secure_filename
import os

#RUTAS

#1 ruta para desplegar el formulario (Debemos de revisar que se haya iniciado sesión)
#HTML con el formulario y todos los inputs a guardar
@app.route('/recipes/new')
def recipes_new():
    #Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    
    return render_template('new.html')


#2 ruta para guardar (Debemos de revisar que se haya iniciado sesión)
#Validar la información
#Guarda la info
@app.route('/recipes/create', methods=['POST'])
def recipes_create():
    #Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    
    #Verificar que el formulario esté llenado correctamente
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')

    #validamos que se alla subido algo
    if "image" not in request.files:
        flash("no selecciono ninguna imagen", "recipe")
        return redirect("/recipes/new")

    
    image = request.files["image"] #variable con la imgen
    if image.fileneme == "":
        flash("nombre de imagen vacio", "recipe")
        return redirect("/recipes/new")

    #generamos de manera segura el nombre de la imagen
    nombre_imagen = secure_filename(image.fileneme)
    #guardamos la imagen
    image.save(os.path.join(app.config["UPLOAD_FOLDER"], nombre_imagen))

    #diccionario con datos del  formulario
    form = {
        "name": request.form["name"],
        "description": request.form["description"],
        "instructions": request.form["instructions"],
        "data_made": request.form["data_made"],
        "under_30": request.form["under_30"],
        "user_id": request.form["user_id"],
        "image": nombre_imagen
    }


    
    #Guardar la informacion
    Recipe.save(form)
    return redirect('/dashboard')

#/recipes/show/3
@app.route('/recipes/show/<int:id>')
def recipes_show(id):
    #Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    
    #Llamar a un método que en base al ID me regrese una instancia de receta
    diccionario = {"id": id}
    recipe = Recipe.get_by_id(diccionario)

    return render_template('show.html', recipe=recipe)

@app.route('/recipes/edit/<int:id>')
def recipes_edit(id):
    #Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    
    diccionario = {"id": id}
    recipe = Recipe.get_by_id(diccionario)

    #Verificar que el usuario en sesión sea es usuario que creo receta
    if recipe.user_id != session['user_id']:
        return redirect('/dashboard')

    return render_template('edit.html', recipe=recipe)

@app.route('/recipes/update', methods=['POST'])
def recipes_update():
    #Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/edit/'+request.form['id'])
    
    #Guardar la actualización
    Recipe.update(request.form)
    return redirect('/dashboard')

@app.route('/recipes/delete/<int:id>')
def recipes_delete(id):
    #Verificar que el usuario haya iniciado sesión
    if 'user_id' not in session:
        flash('Favor de iniciar sesión', 'not_in_session')
        return redirect('/')
    
    #Llamar a un método que reciba el ID y borre ese registro
    diccionario = {"id": id}
    Recipe.delete(diccionario)

    return redirect('/dashboard')
    