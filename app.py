import os
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = 'sqlite:///{}'.format(os.path.join(project_dir, 'mydatabase.db'))

app = Flask(__name__, template_folder='templates1')
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)

class Book(db.Model):
    name = db.Column(db.String(100), unique=True, nullable=False, primary_key=True)
    author = db.Column(db.String(100), nullable=False)
@app.route('/delete', methods=['POST'])
def delete():
    name = request.form['name']
    book = Book.query.filter_by(name=name).first()
    db.session.delete(book)
    db.session.commit()
    return  redirect('/books')
@app.route('/updatebooks')
def updatebooks():
    books = Book.query.all()
    return render_template('update.html',books=books)

@app.route('/update', methods =['POST'])
def update():
    newname = request.form['newname']
    oldname = request.form['oldname']
    newauthor = request.form['newauthor']

    book = Book.query.filter_by(name=oldname).first()
    book.name = newname
    book.author  = newauthor
    db.session.commit()
    return  redirect('/books')
@app.route('/addbook')
def addbook():
    return render_template('addbook.html')

@app.route('/submitbook', methods=['POST'])
def submitbook():
    name = request.form['name']
    author = request.form['author']

    # Create a new Book instance and add it to the database
    new_book = Book(name=name, author=author)
    db.session.add(new_book)
    db.session.commit()
    return redirect('/books')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/profile/<username>')
def profile(username):
    return render_template('profile.html', username=username, isActive=True)

@app.route('/books')
def books():
    books = Book.query.all()

    return render_template('books.html', books=books)

# Create the database tables
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
