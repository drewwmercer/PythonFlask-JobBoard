from multiprocessing import connection
from flask import Flask, g, render_template
import sqlite3

PATH = "db/jobs.sqlite"

# create and configure the app
app = Flask(__name__)


def open_connection():
    connection = getattr(g, '_connection', None)

    if connection == None:
        connection = sqlite3.connect(PATH)
        g._connection = sqlite3.connect(PATH)

    connection.row_factory = sqlite3.Row

    return connection


def execute_sql(sql, values=(), commit=False, single=False):
    connection = open_connection()

    cursor = connection.execute(sql, values)

    if commit == True:
        results = connection.commit()
    else:
        results = cursor.fetchone() if single else cursor.fetchall()

    cursor.close()

    return results


@app.teardown_appcontext
def close_connection(exception):
    connection = getattr(g, '_connection', None)

    if connection != None:
        connection.close()


@app.route('/')
@app.route('/jobs')
def jobs():
    return render_template('index.html')
