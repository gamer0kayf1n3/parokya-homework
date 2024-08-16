from flask import Flask, send_from_directory

app = Flask(__name__)

@app.route("/")
def main():
	return open("index.html").read()
app.run(host="0.0.0.0", port=8000)
