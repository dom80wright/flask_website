from flask import Flask, render_template
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECREY_KEY'] = 'b6c0a55db3c0c6823d510f7e36b1b5e6'

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
    return render_template('home.html', title='Home')
# two 'app.routes' decorators used here as we want the home.html page to come up for both addresses.


@app.route("/blogs")
def blogs():
    return render_template('blogs.html', title='Blogs', posts=posts)


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register") # register details page
def register():
    form = RegistrationForm()
    return render_template('register.html', title='Register', form=form)


@app.route("/login") # login page
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':
    app.run(debug=True)
    # allows you to run your site in debug mode, allowing you to see instant changes.
