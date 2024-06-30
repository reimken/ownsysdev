from WebApp import app
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
 
        for manager in managers:
            if manager['name'] == name and manager['password'] == password:
                session['user_id'] = manager['id']
                flash('Sikeres.', 'success')
                return redirect(url_for('list_all_projects'))

        flash('Sikertelen.', 'danger')

    return render_template('login.html')

#End of login surface

#All projects
@app.route('/projects', methods=['GET'])
def list_all_projects():
 return render_template("projects.html", listed_items=projects)
# End of all projects

@app.route('/projects/type_id=<type_id>', methods=['GET'])
def filtered_projects(type_id):
    filtered_projects = [project for project in projects if project['type_id'] == type_id]
    return render_template('type_id.html', listed_items=filtered_projects)

#Project in details
@app.route('/projects/<int:project_id>', methods=['GET'])
def project_details(project_id):
    project = next((project for project in projects if project['id'] == project_id), None)
    project_tasks = [task for task in tasks if task['project_id'] == project_id]
    return render_template('one_proj.html', project=project, tasks=project_tasks)
#End project in details

# New task
@app.route("/projects/<int:id>/new_task", methods=['GET', 'POST'])
def new_task(id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        developer_id = int(request.form['developer'])

        # Generate new task ID (example)
        new_task_id = len(tasks) + 1
        
        # Create new task object
        new_task = {
            "id": new_task_id,
            "name": name,
            "description": description,
            "project_id": id,
            "user_id": developer_id,
            "deadline": ""  # You can add a deadline field if needed
        }

        # Add new task to tasks list
        tasks.append(new_task)

        # Redirect to project details page after adding task
        return redirect(url_for('project_details', project_id=id))

    # Render the new task form template
    return render_template("new.html", developers=developers)

#Task created by logged in user
@app.route("/tasks_created_by_me")
def created_by_me():
    user_id = session.get('user_id')
    if user_id is None:
        flash('jelentkezzen be!', 'danger')
        return redirect(url_for('login'))
    
    filtered_tasks = [task for task in tasks if task['user_id'] == user_id]
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
       filtered_tasks = [task for task in tasks if task['user_id'] == user_id]
       deadline_tasks = [task for task in filtered_tasks if 'deadline' in task and task['deadline'] and (datetime.strptime(task['deadline'], '%Y-%m-%d %H:%M:%S') - today).days < 4]
   
   return render_template("deadline.html", tasks=deadline_tasks)
#End of deadline filter

#Dummy datas:

managers=[
   {"id": 1, "name": "Imre", "email": "imre@test.com", "password": "test"},
   {"id": 2, "name": "Mate", "email": "mate@test.com", "password": "test"},
   ]

projects = [
    {"id": 1, "name": "1", "type_id": "1", "description": "1"},
    {"id": 2, "name": "2", "type_id": "2", "description": "2"},
    {"id": 3, "name": "3", "type_id": "1", "description": "3"},
    {"id": 4, "name": "4", "type_id": "2", "description": "4"}
]

proj_types = [
   {"type_id": 1, "name": "1" },
   {"type_id": 2, "name": "2" }
    ]
    
tasks = [
    {"id": 1, "name": "Dummy Task 1", "description": "Dummy description for task 1", "project_id": 1, "user_id": 1, "deadline": "2024-07-01 12:00:00"},
    {"id": 2, "name": "Dummy Task 2", "description": "Dummy description for task 2", "project_id": 1, "user_id": 2, "deadline": "2024-07-02 12:00:00"},
    {"id": 3, "name": "Dummy Task 3", "description": "Dummy description for task 3", "project_id": 2, "user_id": 1, "deadline": "2024-07-03 12:00:00"},
    {"id": 4, "name": "Dummy Task 4", "description": "Dummy description for task 4", "project_id": 2, "user_id": 3, "deadline": "2024-07-04 12:00:00"},
    {"id": 5, "name": "Dummy Task 5", "description": "Dummy description for task 5", "project_id": 2, "user_id": 2, "deadline": "2024-07-05 12:00:00"}
]


developers = [
   {"id": 1, "name": "tester1", "email": "tester1@tester.hu"},
   {"id": 2, "name": "tester2", "email": "tester2@tester.hu"}
]