from app import app
from flask import render_template

@app.route('/')
@app.route('/index')
def index():
    user = {'nickname':'Pierre'}
    posts = [  # fake array of posts
        {
            'author': {'nickname': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'nickname': 'Susan'},
            'body': 'Star Wars movie was so cool!' }]
    return render_template('index.html',title='Home',user=user,posts=posts)
