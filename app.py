from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
  tasks = ["Task 1", "Task 2", "Task 3"]  # Example tasks wait to be replaced with actual data
  return render_template('index.html', tasks=tasks[:3])

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/tasks')
def tasks():
    return render_template('tasks.html')

@app.route('/timer')
def timer(): 
    return render_template('timer.html')

@app.route('/leaderboard')
def leaderboard():
    return render_template('leaderboard.html')

if __name__ == '__main__':
    app.run(debug=True)
  