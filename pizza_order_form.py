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
    print(request.method)
    if request.method == 'POST':
        print("enter request method+++++++++++++++++++")
        name = request.form['name'].strip()
        print(name)
        print(request)
        print(request.args)
        print(request.form)
        name12 = request.args.get("name")
        print(name12)
        topping = request.form['topping']
        print(topping)
        sauce = request.form['sauce']
        print(sauce)
        extras = ", ".join(request.form.getlist('extras'))
        print(extras)
        instructions = request.form['instructions'].strip()
        print(instructions)

        # Validate name length (must be between 3 and 20 characters)
        if len(name) < 3 or len(name) > 20:
            print("name length error+++++++++++++++++++")
            abort(404)

        db = get_db()
        try:
            update_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # This is safe because it uses parameterized queries with placeholders (?) and
            # binds user inputs (name, topping, etc.) separately.
            # This prevents SQL injection by ensuring inputs are treated as data, not executable SQL.
            # The ? placeholders and tuple binding ((name, ...) ) ensure SQLite escapes special characters,
            # preventing malicious input (e.g., Robert'; DROP TABLE Orders; --) from altering the query.
            print(update_time)
            db.execute("""
                INSERT INTO Orders (name, topping, sauce, extras, instructions,update_time)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (name, topping, sauce, extras, instructions, update_time))
            print("db.execute")
            db.commit()
            print("db.commit")
        except sqlite3.IntegrityError:
            db.execute("""
                UPDATE Orders
                SET topping=?, sauce=?, extras=?, instructions=?,update_time=?
                WHERE name=?
            """, (topping, sauce, extras, instructions, update_time, name))
            db.commit()
        # except:
        #     print("another except")
        # finally:
        #     print("finally")
        else:
            print("another else")

        return render_template('confirmation.html', name=name)
    return render_template('test.html')


@app.errorhandler(404)
def not_found(e):
    print(e)
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)
