from flask import Flask, render_template
app = Flask(__name__)

# routes are what we type into our browser to go to different pages.

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


if __name__ == '__main__':
    app.run(debug=True)
    # allows you to run your site in debug mode, allowing you to see instant changes.
