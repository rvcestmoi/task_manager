from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from models import db, Task
from utils.auth import login_required, check_credentials
import os

app = Flask(__name__)
app.config.from_object('config.Config')

db.init_app(app)

# Création de la base de données au premier lancement
with app.app_context():
    db.create_all()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']
        if check_credentials(login, password):
            session['user'] = login
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error="Identifiants incorrects")
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    now = datetime.now()
    tasks = Task.query.order_by(Task.next_due).all()

    for task in tasks:
        task.remaining = (task.next_due - now).total_seconds()
        task.status = "ok" if task.remaining > 0 else "late"
    return render_template('index.html', tasks=tasks)

@app.route('/done/<int:task_id>', methods=['POST'])
@login_required
def done(task_id):
    task = Task.query.get(task_id)
    if task:
        task.next_due = datetime.now() + timedelta(hours=task.frequency_hours)
        db.session.commit()
    return '', 204

@app.route('/update_order', methods=['POST'])
@login_required
def update_order():
    data = request.json
    for index, task_id in enumerate(data.get("order", [])):
        task = Task.query.get(task_id)
        if task:
            task.order = index
    db.session.commit()
    return jsonify({"status": "success"})

@app.route('/tasks')
@login_required
def tasks():
    all_tasks = Task.query.order_by(Task.order).all()
    return render_template('tasks.html', tasks=all_tasks)

@app.route('/add_task', methods=['POST'])
@login_required
def add_task():
    name = request.form['name']
    frequency = int(request.form['frequency'])
    next_due = datetime.now() + timedelta(hours=frequency)
    max_order = db.session.query(db.func.max(Task.order)).scalar() or 0
    new_task = Task(name=name, frequency_hours=frequency, next_due=next_due, order=max_order + 1)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/delete_task/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
    return redirect(url_for('tasks'))

@app.route('/edit_task/<int:task_id>', methods=['POST'])
@login_required
def edit_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.name = request.form['name']
        task.frequency_hours = int(request.form['frequency'])
        db.session.commit()
    return redirect(url_for('tasks'))

if __name__ == '__main__':
    app.run(debug=False)
