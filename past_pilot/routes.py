from flask import render_template, url_for, flash, redirect, request, send_file, send_from_directory
from flask_login import login_user, current_user, logout_user, login_required
from past_pilot.forms import SignInForm, SignUpForm, QuestionForm, KeyForm
from past_pilot.key_generator import generate_key
from past_pilot.directory_modifier import *
from past_pilot import app, db, bcrypt
from past_pilot.similarity import *
from past_pilot.models import User
import os


@app.route('/question', methods=['POST', 'GET'])
def index():
    form = QuestionForm()
                                                
    if form.validate_on_submit():
        keys = form.keys.data.replace(' ', '').split(',')
        arr, length = get_similar(form.question.data, keys)
        if length >= 5:
            pdfs = [[os.path.relpath(arr[i][0][0], os.path.abspath(os.path.dirname(__file__))), arr[i][0][1]+1] for i in range(5)]
        else:
            pdfs = [[os.path.relpath(arr[i][0][0], os.path.abspath(os.path.dirname(__file__))), arr[i][0][1]+1] for i in range(length)]
        return render_template('index.html', form=form, pdfs=pdfs)
    
    return render_template('index.html', form=form)


@app.route('/data/<path:filename>')
def data_files(filename):
    return send_from_directory(os.path.join(app.root_path, 'data'), filename)                                            
                                                                                                
@app.route('/')
def welcome():
    return render_template('welcome.html')
                                                
                                                
@app.route('/about')
def about():
    return render_template('about.html')
                                                
                                                
@app.route('/resources', methods=['POST', 'GET'])
def resources():
    form = KeyForm()

    if not current_user.is_authenticated:
        return render_template('login_req.html')
    else:

        try:
            auth_make_dir(current_user, current_user.key)
        except FileExistsError:
            pass

        # owned_length = len(own_dir_searcher(current_user, 0))
        # owned_names = own_dir_searcher(current_user, 0)
        # owned_urls = own_dir_searcher(current_user, 1)

        if current_user.is_authenticated:
            directory_path = os.path.join(get_data_dir(), current_user.key)
                                                        
        files = os.listdir(directory_path)
        action = request.form.get('action', 'view')
                                                
        if action == 'delete':
            filename = request.form['filename']
            file_path = os.path.join(directory_path, filename)

            if os.path.isfile(file_path):
                os.remove(file_path)
                flash(f'File "{filename}" was deleted successfully', 'success')
            else:
                flash(f'File "{filename}" not found', 'danger')
                                                
        elif action == 'upload':
            new_file = request.files['file']
                                                
            if new_file and new_file.filename.endswith('.pdf'):
                new_file.save(os.path.join(directory_path, new_file.filename))
                flash(f'File "{new_file.filename}" was uploaded successfully', 'success')
            else:
                flash('Only PDF files are allowed', 'danger')
                                                
        if form.validate_on_submit():
            keys = form.keys.data.replace(' ', '').split(',')
            list_dirs = fetch_dir(keys)
                                                
            lengths = len(dir_searcher(list_dirs, 0))
            names = dir_searcher(list_dirs, 0,)
            urls = dir_searcher(list_dirs, 1)
                                                
            return render_template('resources.html', form=form, 
                                names=names, urls=urls, 
                                lengths=lengths,files=files)
                                                
        return render_template('resources.html', form=form, 
                           lengths=0, files=files)
                                                
                                                
@app.route('/download/<filename>')
def download_file(filename):
    directory_path = os.path.join(get_data_dir(), current_user.key)
    file_path = os.path.join(directory_path, filename)
                                                
    if os.path.isfile(file_path):
        return send_file(file_path, as_attachment=True)
    else:                                                
        return 'File not found', 404


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
                                                
    form = SignUpForm()
    key = generate_key()
                                                    
    if request.method == 'POST' and form.validate_on_submit():
                                                
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, key=form.key.data)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'success')
                                                
        return redirect(url_for('signin'))
                                                
                                                
    return render_template('signup.html', title='Sign Up', form=form, key=key)
                                                
                                                
@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
                                                
    form = SignInForm()
                                                
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()

        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
                                                
    return render_template('signin.html', title='Sign In', form=form)
                                                
                                                
@app.route("/signout")
def signout():
    logout_user()
    return redirect(url_for('index'))
                                                
                                                
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    return render_template('profile.html', current_user=current_user)






















                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                  
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                 

                                                

