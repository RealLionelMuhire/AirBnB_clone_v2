#!/usr/bin/python3
"""creating some 2 path route"""

from flask import Flask, escape, render_template


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def hello_hbnb():
    """Hello HBNB!"""
    return 'Hello HBNB!'


@app.route('/hbnb', strict_slashes=False)
def hbnb():
    """HBNB"""
    return 'HBNB'


@app.route('/c/<text>', strict_slashes=False)
def c_text(text):  # Fix the parameter name here
    """Replace underscores (_) with spaces"""
    text = text.replace("_", " ")
    return 'C ' + text


@app.route("/python/", defaults={"text": "is cool"}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text):
    """Replacing text with passed one"""
    return "Python " + escape(text.replace("_", " "))


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    """returning a number"""
    return f"{n} is a number"


@app.route("/number_template/<int:n>", strict_slashes=False)
def number_template(n=None):
    """display a HTML page only if n is an integer"""
    if isinstance(n, int):
        return render_template('5-number.html', n=n)


@app.route('/number_odd_or_even/<int:n>', strict_slashes=False)
def odd_or_even(n):
    if n % 2 == 0:
        res = "even"
    else:
        res = "odd"
    return render_template('6-number_odd_or_even.html', n=n, res=res)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
