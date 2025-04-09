from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'hello world'

# Подключение к базе данных SQLite
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Создание таблицы пользователей (если она не существует)
def init_db():
    conn = get_db_connection()
    with app.open_resource('schema.sql') as f:
        conn.executescript(f.read().decode('utf8'))
    conn.commit()
    conn.close()

# Маршрут для отображения и обработки формы
@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Обновление данных пользователя в базе данных
        conn = get_db_connection()
        conn.execute('UPDATE users SET name = ?, email = ?, password = ? WHERE id = 1',
                     (name, email, password))
        conn.commit()
        conn.close()

        flash('Profile updated successfully!', 'success')
        return redirect(url_for('edit_profile'))

    return render_template('edit_profile.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)

