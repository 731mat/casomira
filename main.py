from datetime import datetime
from dateutil import parser
import sqlite3
import datetime

from flask import Flask, flash, g, jsonify, redirect, render_template, request, url_for

DATABASE = '/home/mat/PycharmProjects/casomira/main.db'
DEBUG = True
SECRET_KEY = '\x02\xbb(M\xcd\xdc\xea,7\x02\x00\xdey\x9e?\xa2\x14b\xc8T+\xce\xba\xf7'

app = Flask(__name__)
app.config.from_object(__name__)


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])


@app.before_request
def before_request():
    g.db = connect_db()


@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route('/')
def zakladni():
    pass

@app.route('/people/')
def people_show():
    #bez filtru
    cur = g.db.execute('SELECT p.id, p.startNumber, p.nameFirst, p.nameLast, strftime("%Y-%m-%d",p.birth), c.name as category, p.pay FROM people AS p JOIN category AS c ON p.categoryId = c.id;')

    peoples = [dict(id=row[0], startNumber=row[1], nameFirst=row[2], nameLast=row[3], bith=row[4], category=row[5],pay=row[6]) for row in cur.fetchall()]

    #katogorie -----
    cur = g.db.execute('SELECT * FROM category')
    categorys = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]

    return render_template('people_show.html', peoples=peoples, categorys=categorys)

@app.route('/people/category/<int:category_id>',methods=['GET', 'POST'])
def people_category_show(category_id):
    #bez filtru
    cur = g.db.execute('SELECT p.id, p.startNumber, p.nameFirst, p.nameLast, strftime("%Y-%m-%d",p.birth), c.name as category, p.pay FROM people AS p JOIN category AS c ON p.categoryId = c.id WHERE (p.categoryId) = (?);', str(category_id))

    peoples = [dict(id=row[0], startNumber=row[1], nameFirst=row[2], nameLast=row[3], bith=row[4], category=row[5],pay=row[6]) for row in cur.fetchall()]

    #katogorie -----
    cur = g.db.execute('SELECT * FROM category')
    categorys = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]

    return render_template('people_show.html', peoples=peoples, categorys=categorys)


@app.route('/people/delete/<int:people_id>',methods=['GET', 'POST'])
def people_delete(people_id):
    g.db.execute('delete from people where (id)=(?)', [people_id])
    g.db.commit()
    flash('People was deleted!', 'warning')
    return redirect(url_for('people_show'))


@app.route('/people/edit/<int:people_id>',methods=['GET', 'POST'])
def people_edit(people_id):
    if request.method == 'POST':
        print ('update people set startNumber=(?), nameFirst=(?),nameLast=(?), birth=(?),categoryId=(?),pay=(?) where (id)=(?)',[request.form['startNumber'], request.form['nameFirst'],request.form['nameLast'],request.form['birth'],request.form['categoryId'], people_id])


        g.db.execute('update people set startNumber=(?), nameFirst=(?),nameLast=(?), birth=(?),categoryId=(?),pay=(?) where (id)=(?)',
                     [request.form['startNumber'], request.form['nameFirst'],request.form['nameLast'],request.form['birth'],request.form['categoryId'],request.form['pay'], people_id])
        g.db.commit()
        flash('Project successfully modified.', 'success')
        return redirect(url_for('people_show'))
    else:
        cur = g.db.execute('SELECT p.id, p.startNumber, p.nameFirst, p.nameLast, strftime("%Y-%m-%d",p.birth), c.name as category, p.pay FROM people AS p JOIN category AS c ON p.categoryId = c.id WHERE (p.id) = (?);',str(people_id))
        result = cur.fetchall()[0]
        people = dict(id=result[0], startNumber=result[1], nameFirst=result[2], nameLast=result[3], birth=result[4], category=result[5],pay=result[6])
        # katogorie -----
        cur = g.db.execute('SELECT * FROM category')
        categorys = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
        return render_template('people_edit.html', people=people,categorys=categorys)

@app.route('/people/add/',methods=['GET', 'POST'])
def people_add():
    if request.method == 'POST':
        g.db.execute('insert into people (startNumber, nameFirst, nameLast, birth, categoryId, pay) VALUES (?,?,?,?,?,?)',
                     [request.form['startNumber'], request.form['nameFirst'],request.form['nameLast'],request.form['birth'],request.form['categoryId'],request.form['pay']])
        g.db.commit()
        flash('People ADD.', 'success')
        return redirect(url_for('people_show'))
    else:
        cur = g.db.execute('SELECT * FROM category')
        categorys = [dict(id=row[0], name=row[1]) for row in cur.fetchall()]
        return render_template('people_add.html',categorys=categorys)




if __name__ == '__main__':
    app.run(port=int("3000"))
