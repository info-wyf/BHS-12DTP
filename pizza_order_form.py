from flask import Flask, render_template, request, g, abort
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'pizza.db')


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(app.config['DATABASE'])
        g.db.execute('PRAGMA foreign_keys = ON')
        g.db.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                topping TEXT NOT NULL,
                sauce TEXT NOT NULL,
                extras TEXT,
                instructions TEXT
            )
        """)
        g.db.commit()
    return g.db


@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()


# @app.route('/orderList',methods = ['GET', 'POST'])
# def orderList():
#     db= get_db()
#
#     cur = db.cursor()
#     cur.execute('SELECT id,name,topping,sauce,extras,instructions,update_time FROM Orders ORDER BY id ASC;')
#
#     orderLists = cur.fetchall()
#     print(orderLists)  # DEBUG
#     return render_template('orders_list.html',orders = orderLists)


@app.route('/', methods=['GET', 'POST'])
def order():
    # if request.method == 'POST':
    #     name = request.form['name'].strip()
    #     topping = request.form['topping']
    #     sauce = request.form['sauce']
    #     extras = ", ".join(request.form.getlist('extras'))
    #     instructions = request.form['instructions'].strip()
    #
    # #Validate name length (must be between 3 and 20 characters)
    # if len(name) < 3 or len(name) > 20:
    #     abort(404)
    #
    #     db = get_db()
    #     try:
    #         update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    #         db.execute("""
    #             INSERT INTO Orders (name, topping, sauce, extras, instructions,update_time)
    #             VALUES (?, ?, ?, ?, ?,?)
    #         """, (name, topping, sauce, extras, instructions,update_time))
    #         db.commit()
    #     except sqlite3.IntegrityError:
    #         db.execute("""
    #             UPDATE Orders
    #             SET topping=?, sauce=?, extras=?, instructions=?,update_time=?
    #             WHERE name=?
    #         """, (topping, sauce, extras, instructions,update_time, name))
    #         db.commit()
    #
    #     return render_template('confirmation.html', name=name)
    return render_template('test.html')


@app.errorhandler(404)
def not_found(e):
    print(e)
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)
