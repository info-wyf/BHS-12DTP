from flask import Flask, render_template, request, g, abort
from datetime import datetime
import sqlite3
import os

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.root_path, 'pizza.db')


# Function to get the database connection
# Creates the database and tables if they don't exist
def get_db():
    # Use Flask's application context to store the database connection
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect('pizza.db')
        # db.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
        # Create tables if they don't exist
        c = db.cursor()
        # Pizza table for storing pizza details
        c.execute('''CREATE TABLE IF NOT EXISTS Pizza (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT
                    )''')
        # Topping table for storing topping details
        c.execute('''CREATE TABLE IF NOT EXISTS Topping (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT
                    )''')
        # PizzaTopping table for linking pizzas with toppings
        c.execute('''CREATE TABLE IF NOT EXISTS PizzaTopping (
                        pizza_id INTEGER,
                        topping_id INTEGER,
                        FOREIGN KEY(pizza_id) REFERENCES Pizza(id),
                        FOREIGN KEY(topping_id) REFERENCES Topping(id),
                        PRIMARY KEY (pizza_id, topping_id)
                    )''')
        # Orders table for storing pizza orders
        c.execute('''CREATE TABLE IF NOT EXISTS Orders (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT UNIQUE,
                        topping TEXT,
                        sauce TEXT,
                        extras TEXT,
                        instructions TEXT,
                        update_time TEXT
                    )''')
        db.commit()
    return db


# Close the database connection after each request
@app.teardown_appcontext
def close_db(exception):
    db = getattr(g, '_database', None)
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

@app.route('/delete_order/<int:id>',methods = ['POST'])
def delete_order(id):
    db = get_db()
    db.execute("DELETE FROM Orders WHERE id =?",(id,))
    cursor = db.execute("SELECT * FROM Orders ORDER BY id ASC")
    orderlists = cursor.fetchall()
    db.commit()
    db.close()

    return render_template("test_list.html", orders=orderlists)

# Route to Orders list with search
@app.route('/orderList')
def order_List():
    db = get_db()
    cursor = db.execute("SELECT * FROM Orders ORDER BY id ASC")
    orderlists = cursor.fetchall()
    db.close()
    print(orderlists)
    # for orderlist in orderlists:
    #     print(orderlist)
    #     print(orderlist[0])
    #     print(orderlist[1])
    #     print(orderlist[2])
    return render_template('test_list.html', orders=orderlists)

@app.errorhandler(404)
def not_found(e):
    print(e)
    return render_template("404.html")


if __name__ == '__main__':
    app.run(debug=True)
