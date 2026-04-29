from flask import Flask, render_template, request, jsonify
from app import app, db
from app.models import Task

@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')


@app.route('/get_tasks', methods=['GET'])
def get_tasks():
  tasks = Task.query.all()
  return jsonify({"tasks": [ {"id": task.id, "content": task.content} for task in tasks ]})

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.get_json()
    task_content = data.get('task')

    if task_content:
        new_task = Task(content=task_content)
        db.session.add(new_task)
        db.session.commit()

    tasks = Task.query.all()

    return jsonify({
        "tasks": [
            {"id": t.id, "content": t.content}
            for t in tasks
        ]
    })

@app.route('/delete_tasks/<int:id>', methods=['DELETE'])
def delete_tasks(id):
  task_thing= Task.query.get(id)

  if task_thing:
    db.session.delete(task_thing)
    db.session.commit()

  tasks = Task.query.all()

  return jsonify({"tasks": [ {"id": task.id, "content": task.content} for task in tasks ]})

@app.route('/login')
def login():
  return render_template('login.html')

@app.route('/tasks')
def tasks_page():
  return render_template('tasks.html')

@app.route('/timer')
def timer(): 
  return render_template('timer.html')

@app.route('/leaderboard')
def leaderboard():
  return render_template('leaderboard.html')
