from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('events.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS events
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                     name TEXT,
                     description TEXT,
                     date TEXT,
                     time TEXT,
                     domain TEXT,
                     type TEXT)''')
    conn.close()

@app.route('/')
def index():
    domain = request.args.get('domain')
    type_ = request.args.get('type')
    time = request.args.get('time')

    query = "SELECT * FROM events WHERE 1=1"
    params = []
    if domain:
        query += " AND domain=?"
        params.append(domain)
    if type_:
        query += " AND type=?"
        params.append(type_)
    if time:
        query += " AND time LIKE ?"
        params.append(f'{time}%')

    conn = sqlite3.connect('events.db')
    events = conn.execute(query, params).fetchall()
    conn.close()
    return render_template('index.html', events=events)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'POST':
        data = (request.form['name'], request.form['description'],
                request.form['date'], request.form['time'],
                request.form['domain'], request.form['type'])

        conn = sqlite3.connect('events.db')
        conn.execute('INSERT INTO events (name, description, date, time, domain, type) VALUES (?, ?, ?, ?, ?, ?)', data)
        conn.commit()
        conn.close()
        return redirect('/')
    return render_template('submit.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
