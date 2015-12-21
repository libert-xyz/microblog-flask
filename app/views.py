from app import app
from forms import LoginForm,EditForm
from models import *
from flask import render_template,redirect,flash,url_for,request, g
from flask.ext.login import login_required,logout_user,login_user,current_user
from sqlalchemy import update
from datetime import datetime


@app.before_request
def before_request():
    g.user = current_user
    if g.user == current_user:
        if g.user.is_authenticated:
            g.user.last_seen = datetime.utcnow()
            db.session.add(g.user)
            db.session.commit()



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

        nickname = User.query.filter_by(nickname=form.nickname.data).first()
        password = User.query.filter_by(password=form.password.data).first()


        if nickname:
            login_user(nickname)

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


@app.route('/edit',methods=['GET','POST'])
@login_required
def edit():
    form = EditForm()
    g.user = current_user
    if form.validate_on_submit():
        g.user.nickname=form.nickname.data
        g.user.about_me=form.about_me.data
        db.session.add(g.user)

        db.session.commit()
        flash("Profile Update")
        return redirect(url_for('index'))
    else:
        flash("An error has ocurred")

    return render_template('edit.html',form=form)



@app.route('/logout')
def logout():

    logout_user()
    return redirect(url_for('index'))
