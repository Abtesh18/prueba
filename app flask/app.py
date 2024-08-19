from flask import Flask, request, render_template, redirect, url_for, flash
import redis
import json

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Necesario para usar las funcionalidades de flash
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

def get_recipe(name):
    recipe = redis_client.hget('recetas', name)
    return json.loads(recipe) if recipe else None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add', methods=['GET', 'POST'])
def add_recipe():
    if request.method == 'POST':
        name = request.form['name']
        ingredients = request.form['ingredients'].split(',')
        steps = request.form['steps'].split(';')
        
        recipe = {
            'nombre': name,
            'ingredientes': [i.strip() for i in ingredients],
            'pasos': [p.strip() for p in steps if p.strip()]
        }
        
        redis_client.hset('recetas', name, json.dumps(recipe))
        flash('Receta añadida con éxito.')
        return redirect(url_for('index'))
    
    return render_template('add_recipe.html')

@app.route('/update', methods=['GET', 'POST'])
def update_recipe():
    if request.method == 'POST':
        old_name = request.form['old_name']
        new_name = request.form['new_name']
        new_ingredients = request.form['new_ingredients']
        new_steps = request.form['new_steps']
        
        recipe = get_recipe(old_name)
        if recipe:
            if new_name:
                redis_client.hdel('recetas', old_name)
                old_name = new_name
            if new_ingredients:
                recipe['ingredientes'] = [i.strip() for i in new_ingredients.split(',')]
            if new_steps:
                recipe['pasos'] = [p.strip() for p in new_steps.split(';') if p.strip()]
            
            redis_client.hset('recetas', old_name, json.dumps(recipe))
            flash('Receta actualizada con éxito.')
        else:
            flash('Receta no encontrada.')
        
        return redirect(url_for('index'))
    
    return render_template('update_recipe.html')

@app.route('/delete', methods=['POST'])
def delete_recipe():
    name = request.form['name']
    if redis_client.hdel('recetas', name):
        flash('Receta eliminada con éxito.')
    else:
        flash('Receta no encontrada.')
    return redirect(url_for('index'))

@app.route('/list')
def list_recipes():
    recipes = redis_client.hgetall('recetas')
    recipes = {name: json.loads(recipe) for name, recipe in recipes.items()}
    return render_template('list_recipes.html', recipes=recipes)

@app.route('/search', methods=['GET', 'POST'])
def search_recipe():
    if request.method == 'POST':
        name = request.form['name']
        recipe = get_recipe(name)
        if recipe:
            return render_template('search_recipe.html', recipe=recipe)
        else:
            flash('Receta no encontrada.')
    
    return render_template('search_recipe.html')

if __name__ == '__main__':
    app.run(debug=True)
