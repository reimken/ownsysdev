from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from WebApp import app, db
from WebApp.models import Manager, Project, Task, Developer
from datetime import datetime, timedelta
import datetime
from . import UserRoles
import jwt

def manager_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') != UserRoles.MANAGER:
            flash('Managers only!', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def user_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_role') not in [UserRoles.MANAGER, UserRoles.USER]:
            flash('User only!', 'danger')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        print("feltetel elott")
        # Ellenõrizzük, hogy van-e 'Authorization' fejléc a kérésben
        if 'Authorization' in request.headers:
            print("feltetelben")
            parts = request.headers['Authorization'].split()
            if len(parts) == 2 and parts[0] == 'Bearer':
                token = parts[1]
        print(token)
        if not token:
            print()
            return jsonify({'message': 'Token missing!'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = data['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Expired token!'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

# Login surface
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        data = request.json
        print(data)
        # Ellenõrizzük, hogy a 'name' és 'password' jelen van-e a JSON adatban
        if not data or 'name' not in data or 'password' not in data:
            return jsonify({'message': 'Missing name or password'}), 400
        
        name = data['name']
        password = data['password']
        user = db.session.query(Manager).filter_by(name=name, password=password).first()
        
        if user:
            session['user_id'] = user.id
            session['user_role'] = UserRoles.MANAGER if user.id == 1 else UserRoles.USER
            token = generate_token(user.id)
            print(token)
            return jsonify({'message': 'Successful login.', 'token': token})
        else:
            return jsonify({'message': 'Unsuccessful login.'}), 401

    # Ha a kérés nem POST, akkor rendereljük a bejelentkezési oldalt
    return render_template('login.html')

def generate_token(user_id):
    try:
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1), 
            'iat': datetime.datetime.utcnow(),
            'sub': user_id  
        }
        token = jwt.encode(payload, app.config['SECRET_KEY'], algorithm='HS256')
        return token
    except Exception as e:
        return str(e)


# All projects
@app.route('/projects', methods=['GET'])
@token_required
def list_all_projects():
    projects = db.session.query(Project).all()
    return render_template("projects.html", listed_items=projects)

# Project filter by type_id
@app.route('/projects/type_id=<type_id>', methods=['GET'])
@user_required
def filtered_projects(type_id):
    filtered_projects = db.session.query(Project).filter_by(type_id=type_id).all()
    return render_template('type_id.html', listed_items=filtered_projects)

# Project in details
@app.route('/projects/<int:project_id>', methods=['GET'])
@user_required
def project_details(project_id):
    project = db.session.query(Project).filter_by(id=project_id).first()
    filtered_tasks = db.session.query(Task).filter_by(project_id=project_id).all()
    return render_template('one_proj.html', project=project, tasks=filtered_tasks)

# New task


@app.route("/projects/<int:id>/new_task", methods=['GET', 'POST'])
@manager_required
def new_task(id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        developer_id = int(request.form['developer'])
        project = Project.query.get_or_404(id)
        developer = Developer.query.get_or_404(developer_id)
        new_task = Task(name=name, description=description, project_id=id, user_id=developer_id)
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('project_details', project_id=id))

    developers = Developer.query.all()
    return render_template("new.html", developers=developers)

# Task created by logged in user
@app.route("/tasks_created_by_me")
@manager_required
def created_by_me():
    user_id = session.get('user_id')
    if user_id is None:
        flash('Log in', 'danger')
        return redirect(url_for('login'))
    
    filtered_tasks = db.session.query(Task).filter_by(user_id=user_id).all()
    return render_template("byme.html", tasks=filtered_tasks)

# Deadline filter
@app.route("/task_filtered_by_deadline")
@manager_required
def filtered_by_deadline():
    user_id = session.get('user_id')
    if user_id is None:
        flash('Log in!', 'danger')
        return redirect(url_for('login'))
    today = datetime.now()
    deadline_limit = today + timedelta(days=4)
    deadline_tasks = db.session.query(Task).filter(
        Task.user_id == user_id,
        Task.deadline != None,
        Task.deadline <= deadline_limit
    ).all()
    return render_template("deadline.html", tasks=deadline_tasks)
