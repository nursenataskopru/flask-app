from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'gizli_anahtar'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row 
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/quiz', methods=['GET'])
def quiz():
    conn = get_db_connection()
    questions = conn.execute('SELECT * FROM questions').fetchall()
    
    questions_with_options = []
    for question in questions:
        options = conn.execute('SELECT option_text FROM options WHERE question_id = ?', (question['id'],)).fetchall()
        questions_with_options.append({
            'id': question['id'],
            'question_text': question['question_text'],
            'options': [option['option_text'] for option in options]
        })
    
    conn.close()
    return render_template('quiz.html', questions=questions_with_options)

@app.route('/submit', methods=['POST'])
def submit():
    conn = get_db_connection()
    
    user_answers = {key: request.form[key] for key in request.form.keys() if key.startswith('q')}
    
    score = 0
    for question_id, answer in user_answers.items():
        question_id = question_id[1:]
        correct_answer = conn.execute('SELECT correct_answer FROM questions WHERE id = ?', (question_id,)).fetchone()
        if correct_answer and answer.strip() == correct_answer['correct_answer']:
            score += 10
    
    username = session.get('username', 'guest')
    user = conn.execute('SELECT * FROM users WHERE username = ?', (username,)).fetchone()
    
    if user:
        if score > user['highest_score']:
            conn.execute('UPDATE users SET highest_score = ? WHERE username = ?', (score, username))
            conn.commit()
            session['high_score'] = score
        else:
            session['high_score'] = user['highest_score']
    else:
        conn.execute('INSERT INTO users (username, highest_score) VALUES (?, ?)', (username, score))
        conn.commit()
        session['high_score'] = score

    conn.close()
    
    session['score'] = score
    
    return redirect(url_for('results'))

@app.route('/results')
def results():
    score = session.get('score', 0)
    high_score = session.get('high_score', 0)
    return render_template('results.html', score=score, high_score=high_score)

if __name__ == '__main__':
    app.run(debug=True)
