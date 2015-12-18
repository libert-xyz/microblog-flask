from app import app
from forms import LoginForm
from models import *
from flask import render_template,redirect,flash,url_for,request
from flask.ext.login import login_required,logout_user,login_user


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

@app.route('/login',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():

        nickname = User.query.filter_by(nickname=request.form['nickname']).first()
        password = User.query.filter_by(password=request.form['password']).first()

        login_user(nickname)

        if nickname is not None and password is not None:
        #if request.form['nickname'] == 'admin' and request.form['password'] == 'admin':
            flash('Login requested for OpenID="%s", remember_me=%s' %
                  (form.nickname.data, str(form.remember_me.data)))
            return redirect('/index')
        else:
            flash('Invalid User or Password')

    return render_template('login.html',title="Sign in",form=form)


@app.route('/user/<nickname>')
@login_required
def users(nickname):

    user = User.query.filter_by(nickname=nickname).first()
    if user == None:
        flash("User %s not found." %nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}]
    return render_template('user.html',user=user,posts=posts)

@app.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('index'))
