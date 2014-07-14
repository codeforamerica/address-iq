from flask import Flask, render_template
import os

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

@app.route("/")
def home():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(debug=True)
