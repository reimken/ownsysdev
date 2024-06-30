from WebApp import app, models, db
from WebApp.models import Manager, Project, Task, Developer
from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta

app.secret_key = 'rendszerfejlesztes'

#Login surface
@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        user = db.session.query(Manager).filter_by(name=name, password=password).first()   
        print(user)
        if user:
            session['user_id'] = user.id
            flash('Sikeres.', 'success')
            return redirect(url_for('list_all_projects'))
        flash('Sikertelen.', 'danger')
  return render_template('login.html')
#End of login surface

#All projects
@app.route('/projects', methods=['GET'])
def list_all_projects():
 projects = db.session.query(Project).all()
 return render_template("projects.html", listed_items=projects)
# End of all projects

#Project filter by type_id
@app.route('/projects/type_id=<type_id>', methods=['GET'])
def filtered_projects(type_id):
    filtered_projects = db.session.query(Project).filter_by(type_id=type_id).all()
    return render_template('type_id.html', listed_items=filtered_projects)
#End of Project filter by type_id

#Project in details
@app.route('/projects/<int:project_id>', methods=['GET'])
def project_details(project_id):
   project=db.session.query(Project).filter_by(id=project_id).first()
   filtered_tasks= db.session.query(Task).filter_by(project_id=project_id).all()
   print(filtered_tasks)
   return render_template('one_proj.html', project=project, tasks=filtered_tasks)
#End project in details

# New task
@app.route("/projects/<int:id>/new_task", methods=['GET', 'POST'])
def new_task(id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        developer_id = int(request.form['developer'])
        # Find the project by id
        project = Project.query.get_or_404(id)
        # Find the developer by id
        developer = Developer.query.get_or_404(developer_id)
        # Create a new task object
        new_task = Task(name=name, description=description, project_id=id, user_id=developer_id)
        # Add new task to the database session
        db.session.add(new_task)
        db.session.commit()
        # Redirect to project details page after adding task
        return redirect(url_for('project_details', project_id=id))

    # Fetch all developers for the form
    developers = Developer.query.all()

    # Render the new task form template with developers list
    return render_template("new.html", developers=developers)

#Task created by logged in user
@app.route("/tasks_created_by_me")
def created_by_me():
    user_id = session.get('user_id')
    if user_id is None:
        flash('jelentkezzen be!', 'danger')
        return redirect(url_for('login'))
    
    filtered_tasks = db.session.query(Task).filter_by(user_id=user_id).all()
    return render_template("byme.html", tasks=filtered_tasks)
#End of task creation

#Deadline filter
@app.route("/task_filtered_by_deadline")
def filtered_by_deadline():
   user_id = session.get('user_id')
   if user_id is None:
        flash('jelentkezzen be!', 'danger')
        return redirect(url_for('login'))
   else:
       today = datetime.now()
       deadline_limit = today + timedelta(days=4)
       deadline_tasks = db.session.query(Task).filter(
            Task.user_id == user_id,
            Task.deadline != None,
            Task.deadline <= deadline_limit
        ).all()
   
   return render_template("deadline.html", tasks=deadline_tasks)
#End of deadline filter