import requests
from flask import Flask, render_template, request
import datetime


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/joke", methods=["GET", "POST"])
def joke():
    jokes = ""
    message = ""
    mood = None
    if request.method == "POST":
        mood = request.form.get("mood").lower()
        response = requests.get(

            "https://icanhazdadjoke.com/",

            headers={"Accept": "application/json"}

        )
        if response.status_code == 200:  # we successfully got a response
            data = response.json()
            jokes = data["joke"]
        else:
            jokes = "Could not fetch a dad joke right now. Try again later"
        if mood == "happy":
            message = "You deserve Depression"
        elif mood == "sad":
            message = "You deserve not sad"
        elif mood == "stressed":
            message = "You deserve not stressed"
        elif mood == "bored":
            message = "You deserve not bored"

    return render_template("joke.html", jokes=jokes, message=message)


@app.route('/search', methods=['GET', 'POST'])
def search():
    jokes = []
    no_jokes = False
    if request.method == 'POST':
        term = request.form.get('term')
        res = requests.get(
            f"https://icanhazdadjoke.com/search?term={term}",
            headers={"Accept": "application/json"}
        )
        data = res.json()
        if data['total_jokes'] > 0:
            jokes = [j['joke'] for j in data['results']]
        else:
            no_jokes = True
    return render_template('search.html', jokes=jokes, no_jokes=no_jokes)


if __name__ == "__main__":
    app.run(debug=True)
