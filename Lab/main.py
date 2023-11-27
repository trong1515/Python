import pymongo
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient

app = Flask(__name__)
cluster = MongoClient("mongodb://localhost:27017/")
db = cluster["CSDL"]
collection = db["movies"]

@app.route('/')
def index():
    data = collection.find()
    return render_template('text.html', data = data)

@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        _id = request.form['_id']
        name = request.form['name']
        year = int(request.form['year'])
        genre = request.form.getlist('genre')
        description = request.form['description']
        rating = int(request.form['rating'])
        review_date = datetime.now()
        actor_name = request.form['actor_name']
        actor_age = int(request.form['actor_age'])
        new_movie = {
            '_id': _id,
            'name': name,
            'year': year,
            'genre': genre,
            'description': description,
            'reviews': [{'rating': rating, 'date': review_date}],
            'active': True,
            'actor': {'name': actor_name, 'age': actor_age},
            'fullname': f'{name} {year}',
            'convertedYear': year
            }
            
        collection.insert_one(new_movie)
        return redirect(url_for('index'))
    return render_template('add.html')


@app.route('/edit/<string:item_id>', methods=['GET', 'POST'])
def edit(item_id):
    item = collection.find_one({"_id": item_id})
    if request.method == 'POST':
        _id = request.form['_id']
        name = request.form['name']
        year = int(request.form['year'])
        genre = request.form.getlist('genre')
        description = request.form['description']
        rating = int(request.form['rating'])
        review_date = datetime.now()
        actor_name = request.form['actor_name']
        actor_age = int(request.form['actor_age'])
        new_values = {
            '_id': _id,
            'name': name,
            'year': year,
            'genre': genre,
            'description': description,
            'reviews': [{'rating': rating, 'date': review_date}],
            'active': True,
            'actor': {'name': actor_name, 'age': actor_age},
            'fullname': f'{name} {year}',
            'convertedYear': year
        }

        collection.update_one({"_id": item_id}, {"$set": new_values})

        return redirect(url_for('index'))

    return render_template('edit.html', item=item)

@app.route('/delete/<string:item_id>')
def delete(item_id):
    collection.delete_one({"_id": item_id})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)