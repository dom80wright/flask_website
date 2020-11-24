from datetime import datetime
from flask import Flask, render_template, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'b6c0a55db3c0c6823d510f7e36b1b5e6'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db' # three slashes are a relative path.

db = SQLAlchemy(app) # create database instance.


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False) # max string size of 60 because passwords will be hashed.
    posts = db.relationship('Post', backref="author", lazy=True) # creates a relationship to the post table below. "backref" creates the attribute "author" for posts created below which will return the associated User info.
    
    def __repr__(self):
        return "User {}, {}, {}.".format(self.username, self.email, self.image_file)
 
class Post(db.Model):    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) # no parentheses as we want the function to run when called, not the time now.
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False) # ID of the user that authored the post.

    def __repr__(self):
        return "Post {}, {}.".format(self.title, self.date_posted)

'''
creating the database and adding entries:
1) to create a database (db file) in your directory, go to terminal, launch python and input "from flaskblog import db" (the SQLAlchemy object created near the top)
2) "db.create_all()" - creates the database.
3) "from flaskblog import User, Post" (name of the models)
create users:
4) "user_x = User(username='Dom', email='email@example.com', password='Password')" to create users. note that id was not submitted. as id is a primary key, the programme will asign the user a unique id automatically. image_file not required.
5) "db.session.add(user_1)" which doesn't actually update the db file, but stages the change ready for commit.

create posts:
6) "post_1 = Post(title='Blog 1', content='First Post Content!', user_id=user.id)"
7) "db.session.add(post_1)"

commit all:
8) "db.session.commit()" to commit all in staging area to the database.

querying the datase:
1) "User.query.all() / User.query.first()" to return all the users / first user in the database.
2) "User.query.filter_by(username="Dom").all() / first()" returns all entries that satisfy the criteria. 
3) "user1 = User.query.filter_by(username="Dom").first()"; "print(user.id)" attach result to a variable, the attributes of which can be accessed like an object.
4) "user = User.query.get(1)" to return the entry with unique id == 1. Can you 'get' more than just userid?

delete / clear the database:
1) "db.drop_all()" - drops / deletes all database tables and rows / data.
2) "db.create_all()" - to recreate the database structure ready for data to be added.
'''

posts = [
    {
        'author': 'James White',
        'email': 'james@madeup.com',
        'title': 'First Post!',
        'content': 'This is the content of the first post.',
        'date_posted': 'November 10th, 2020'
    },
    {
        'author': 'Katy Smith',
        'email': 'katy@example.com',
        'title': 'Second Post!',
        'content': 'This is some more great content.',
        'date_posted': 'November 11th 2020'
    }
]

# routes are what we type into our browser to go to different pages.


@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', title='Home', posts=posts)
# two 'app.routes' decorators used here as we want the home.html page to come up for both addresses.


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST']) # register details page. methods allows people to get and post back.
def register():
    form = RegistrationForm()
    if form.validate_on_submit(): # if the form submission was successful.
        flash("Account created for {}!".format(form.username.data), 'success') # message to be sent to user.
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST']) # login page
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

if __name__ == '__main__':
    app.run(debug=True)
    # allows you to run your site in debug mode, allowing you to see instant changes.
