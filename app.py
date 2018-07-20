from flask import Flask, request, flash, url_for, redirect, render_template, session
from flask_sqlalchemy import SQLAlchemy
import os
from functools import wraps
from sqlalchemy import or_


#forms imports
from forms import SignUpForm, LoginForm, CommentForm, JobPostForm
from passlib.hash import sha256_crypt

#configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL','postgresql://pi:aduuna14@localhost:5432/ejuma')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = "random string"

db = SQLAlchemy(app)

import models


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'logged_in' not in session:
            flash('loggin required', 'danger')
            return redirect(url_for('login', next=request.url))
        else:
            return f(*args, **kwargs)
    return decorated_function



@app.route('/login', methods=('GET', 'POST'))
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.query(models.Freelancer).filter_by(email=request.form['email']).first()
        if sha256_crypt.verify(request.form['password'], user.password):
            flash('logged in as {}'.format(user.firstname), 'success')
            session['logged_in'] = True
            session['user'] = user.as_dict()
            return redirect(url_for('jobs_index'))
        else:
    	    flash('Failed to login', 'danger')
        
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.clear()
    flash('You have logged out', 'success')
    return redirect(url_for('login'))


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = models.Freelancer(request.form['firstname'],
            request.form['lastname'],
            request.form['contact'],
            request.form['skills'],
            request.form['dob'],
            request.form['status'],
            request.form['email'],
            sha256_crypt.encrypt(request.form['password']),
            )
        db.session.add(user)
        db.session.commit()
        flash('successfully registered', 'success')
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)


@app.route('/profile/<user_id>', methods = ['GET', 'POST'])
@login_required
def view_profile(user_id):
    user = db.session.query(models.Freelancer).get(int(user_id))
    return render_template('profile.html', user=user)



@app.route('/profile/<user_id>/edit', methods = ['GET', 'POST'])
@login_required
def edit_profile(user_id):
    print(user_id,int(session['user']['id']))
    if int(user_id) != int(session['user']['id']):
	    flash('Access Denied! You cannot Edit this profile', 'danger')
	    return redirect(url_for('view_profile', user_id=user_id))
    user_get = db.session.query(models.Freelancer).filter_by(id=int(user_id))
    form = SignUpForm(obj=user_get)
    if request.method == 'POST':
        user = {'firstname':request.form['firstname'],
            'lastname':request.form['lastname'],
            'contact':request.form['contact'],
            'skills':request.form['skills'],
            'dob':request.form['dob'],
            'status':request.form['status'],
            'email':request.form['email'],
            'password':form.password.data,
            }
        
        user_get.update(user)
        db.session.commit()
        flash('Profile Data updated', 'success')
        return redirect(url_for('view_profile', user_id=user_id))
    return render_template('edit_profile.html', form=form)

@app.route('/jobs/search', methods=['GET', 'POST'])
@app.route('/jobs')
def jobs_index():
    if request.method == 'POST':
        heading = 'Search Results'
        string = request.form['query']
        job_list = db.session.query(models.Job_postings).filter(or_(
                        Job_postings.title.contains(string),
                        Job_postings.title.contains(string)
                        ))
    else:
        heading = 'Recent Job Post'
        job_list = user = db.session.query(models.Job_postings).all()
    return render_template('jobindex.html', job_list=job_list, heading=heading)

@app.route('/jobs/<job_id>')
def job_detail(job_id):
	job = user = db.session.query(models.Job_postings).filter_by(id=int(job_id)).first()
	return render_template('job_detail.html', Job_postings=job)

@app.route('/jobs/new', methods = ['GET', 'POST'])
@login_required
def new_job():
    form = JobPostForm()
    if request.method == 'POST' and form.validate_on_submit():
        job = models.Job_postings(
            session.user.id,#employer_id
            request.form['amount'],
            request.form['title'],
            request.form['description'],
            request.form['duration'],
            request.form['no_of_people'],
            )
        db.session.add(job)
        db.session.commit()
        flash('successfully added new job', 'success')
        return redirect(url_for('jobs_index'))
    return render_template('new_job.html', form=form)



@app.route('/about')
def about():
    return redirect('/home#about')


@app.route('/')
@app.route('/home')
def index():
    return render_template('index.html')




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT',5000)))
