from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

task_list = ["1","2","3","5"] #temporary storage for tasks, replace with database in production

@app.route('/', methods=['GET', 'POST'])
def index():
  return render_template('index.html')


@app.route('/get_tasks', methods=['GET'])
def get_tasks():
  return jsonify({"tasks": task_list})


@app.route('/add_task', methods=['POST'])
def add_task():
  data= request.get_json()
  task = data.get('task')

  if task:
    task_list.append(task)

  return jsonify({"tasks": task_list})

@app.route('/delete_tasks/<int:index>', methods=['DELETE'])
def delete_tasks(index):
  if 0 <= index < len(task_list):
    task_list.pop(index)

  return jsonify({"tasks": task_list})

@app.route('/login')
def login():
  return render_template('login.html')

# @app.route('/tasks')
# def tasks_page():
#   return render_template('tasks.html')

@app.route('/timer')
def timer(): 
  return render_template('timer.html')

@app.route('/leaderboard')
def leaderboard():
  return render_template('leaderboard.html')

if __name__ == '__main__':
  app.run(debug=True)
  